// Mikrofon erişimini başlat
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  const audioContext = new AudioContext();
  const source = audioContext.createMediaStreamSource(stream);
  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 256;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);
  source.connect(analyser);

  function animateBubbles() {
      analyser.getByteFrequencyData(dataArray);
      const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
      
      document.querySelectorAll('.bubble').forEach(bubble => {
          const scale = Math.min(1 + average / 128, 2); // Ortalama değeri ölçek olarak kullan
          bubble.style.transform = `scale(${scale})`;
      });

      requestAnimationFrame(animateBubbles);
  }

  animateBubbles();
}).catch(err => {
  console.error('Mikrofona erişim sağlanamadı:', err);
});
