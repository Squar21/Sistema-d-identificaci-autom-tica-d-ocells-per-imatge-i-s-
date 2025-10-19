import React, { useRef, useEffect, useState } from "react";
import Hls from "hls.js";

const VideoStream = () => {
  const videoRef = useRef(null);
  const [info, setInfo] = useState(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [nomsEspecies, setNomsEspecies] = useState({});

  const idVideo = 24;
  const apiBaseUrl = "http://10.192.170.91:8080";

  useEffect(() => {
    const video = videoRef.current;
    const hls = new Hls();
    const streamUrl = `${apiBaseUrl}/hls/stream.m3u8`;

    if (Hls.isSupported()) {
      hls.loadSource(streamUrl);
      hls.attachMedia(video);

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play();
      });

      hls.on(Hls.Events.ERROR, (event, data) => {
        console.error("Error HLS.js: ", data);
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              hls.startLoad();
              break;
            case Hls.ErrorTypes.MEDIA_ERROR:
              hls.recoverMediaError();
              break;
            default:
              hls.destroy();
              break;
          }
        }
      });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = streamUrl;
      video.addEventListener("loadedmetadata", () => video.play());
    } else {
      console.error("HLS no suportat en aquest navegador");
    }

    const timeUpdateHandler = () => {
      setCurrentTime(video.currentTime);
    };

    video.addEventListener("timeupdate", timeUpdateHandler);

    return () => {
      hls.destroy();
      video.removeEventListener("timeupdate", timeUpdateHandler);
    };
  }, []);

  useEffect(() => {
    if (currentTime === 0) return;

    const fetchInfo = async () => {
      try {
        const response = await fetch(
          `${apiBaseUrl}/avistaments/video/${idVideo}?temps=${currentTime}`
        );
        if (!response.ok) throw new Error("Error al fer fetch dels avistaments");
        const data = await response.json();
        setInfo(data);

        // Demana nom_comu per a cada ID únic
        const especiesUnicas = [...new Set(data.map((item) => item.IDEspecie))];
        const nousNoms = { ...nomsEspecies };

        for (const id of especiesUnicas) {
          if (!nousNoms[id]) {
            const res = await fetch(`${apiBaseUrl}/especies/${id}`);
            if (res.ok) {
              const especie = await res.json();
              nousNoms[id] = especie.nom_comu;
            } else {
              nousNoms[id] = "Desconeguda";
            }
          }
        }

        setNomsEspecies(nousNoms);
      } catch (error) {
        console.error(error);
        setInfo(null);
      }
    };

    const timer = setTimeout(fetchInfo, 1000);
    return () => clearTimeout(timer);
  }, [currentTime]);

  return (
    <div style={{ display: "flex", gap: "20px" }}>
      <div style={{ flex: 2 }}>
        <h2>Retransmissió en directe</h2>
        <video
          ref={videoRef}
          controls
          muted
          width="100%"
          style={{ border: "2px solid #000", borderRadius: "10px" }}
        />
      </div>
      <div
        style={{
          flex: 1,
          border: "2px solid #000",
          borderRadius: "10px",
          padding: "10px",
          height: "360px",
          overflowY: "auto",
          fontFamily: "monospace",
          backgroundColor: "#726b6b75",
        }}
      >
        <h3>Informació deteccions</h3>
        {info ? (
          Array.isArray(info) && info.length > 0 ? (
            info.map((item, idx) => (
              <div key={idx} style={{ marginBottom: "10px" }}>
                <div><strong>Espècie:</strong> {nomsEspecies[item.IDEspecie] || item.IDEspecie}</div>
                <div><strong>Àudio:</strong> {item.es_audio ? "🔊" : "🔇"}</div>
                <div><strong>Confiança:</strong> {item.confianza}</div>
              </div>
            ))
          ) : (
            <div>No hi ha avistaments a aquest temps.</div>
          )
        ) : (
          <div>Carregant info...</div>
        )}
      </div>
    </div>
  );
};

export default VideoStream;
