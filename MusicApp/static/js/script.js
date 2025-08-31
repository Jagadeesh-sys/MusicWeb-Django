var currentSongId = null;
var isPlaying = false;
var songItems = document.querySelectorAll('.song-item');

function playSong(songUrl, imageUrl, songId, songName, artistName) {
    var audioPlayer = document.getElementById('audio-player');
    var songImage = document.getElementById('footer-image');
    var footer = document.getElementById('footer');

    audioPlayer.src = songUrl;
    audioPlayer.play();

    songImage.src = imageUrl;
    footer.style.display = 'flex';

    currentSongId = songId;
    isPlaying = true;

    // Set the track name and artist
    document.getElementById('track-name').textContent = songName;
    document.getElementById('artist-name').textContent = artistName;

    // Set the like button action based on songId
    var likeButton = document.querySelector('.like-symbol');
    likeButton.onclick = function() {
        // Implement like functionality here
        alert('Liked song with ID: ' + songId);
    };
    
    // Play next song when current song ends
    audioPlayer.onended = function() {
        var nextSongId = getNextSongId('next');
        var nextSong = document.querySelector(`[data-song-id="${nextSongId}"]`);
        playSong(nextSong.dataset.songUrl, nextSong.dataset.imageUrl, nextSongId, nextSong.dataset.songName, nextSong.dataset.artistName);
    };
}

function togglePlayPause() {
    var audioPlayer = document.getElementById('audio-player');
    var playPauseIcon = document.getElementById('play-pause');

    if (isPlaying) {
        audioPlayer.pause();
        playPauseIcon.innerHTML = '&#9654;'; // play icon
    } else {
        audioPlayer.play();
        playPauseIcon.innerHTML = '&#10074;&#10074;'; // pause icon
    }

    isPlaying = !isPlaying;
}

function getNextSongId(direction) {
    var currentIndex = Array.from(songItems).findIndex(item => item.dataset.songId === currentSongId);
    var nextIndex = direction === 'next' ? (currentIndex + 1) % songItems.length : (currentIndex - 1 + songItems.length) % songItems.length;
    return songItems[nextIndex].dataset.songId;
}

document.getElementById('play-pause').addEventListener('click', togglePlayPause);

document.getElementById('next-song').addEventListener('click', function() {
    var nextSongId = getNextSongId('next');
    var nextSong = document.querySelector(`[data-song-id="${nextSongId}"]`);
    playSong(nextSong.dataset.songUrl, nextSong.dataset.imageUrl, nextSongId, nextSong.dataset.songName, nextSong.dataset.artistName);
});

document.getElementById('prev-song').addEventListener('click', function() {
    var prevSongId = getNextSongId('prev');
    var prevSong = document.querySelector(`[data-song-id="${prevSongId}"]`);
    playSong(prevSong.dataset.songUrl, prevSong.dataset.imageUrl, prevSongId, prevSong.dataset.songName, prevSong.dataset.artistName);
});
