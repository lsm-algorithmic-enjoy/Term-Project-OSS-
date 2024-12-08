document.addEventListener('DOMContentLoaded', () => {
    let currentSequence = null;
    let isPlaying = false;
    const synth = new Tone.Synth().toDestination();

    try {
        const compositionElement = document.getElementById('composition-data');
        const compositionData = JSON.parse(compositionElement.dataset.composition);
        const descriptionElement = document.getElementById('description');
        descriptionElement.textContent = compositionData.description;

        const playButton = document.getElementById('playButton');
        const stopButton = document.getElementById('stopButton');

        playButton.addEventListener('click', async () => {
            if (!compositionData.notes || compositionData.notes.length === 0) {
                alert('재생할 음악이 없습니다.');
                return;
            }

            if (isPlaying) return;

            try {
                await Tone.start(); // 오디오 컨텍스트 시작
                isPlaying = true;

                // 기존 시퀀스 정리
                if (currentSequence) {
                    currentSequence.dispose();
                    currentSequence = null;
                }

                Tone.Transport.stop();
                Tone.Transport.cancel();

                // 템포 설정
                Tone.Transport.bpm.value = compositionData.tempo || 120;

                // 새로운 음악 시퀀스 생성 및 시작
                currentSequence = new Tone.Sequence((time, note) => {
                    synth.triggerAttackRelease(note, '8n', time);
                }, compositionData.notes).start(0);

                Tone.Transport.start();
            } catch (error) {
                console.error('음악 재생 중 오류 발생:', error);
                alert('음악 재생 중 오류가 발생했습니다.');
            }
        });

        stopButton.addEventListener('click', () => {
            if (!isPlaying) return;

            Tone.Transport.stop();
            Tone.Transport.cancel();

            if (currentSequence) {
                currentSequence.dispose();
                currentSequence = null;
            }

            isPlaying = false;
        });

    } catch (error) {
        console.error('음악 데이터 처리 중 오류 발생:', error);
        document.getElementById('description').textContent =
            '음악 데이터를 불러오는 중 오류가 발생했습니다.';
    }
}); 