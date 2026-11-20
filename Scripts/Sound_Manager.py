import pygame
from Settings import *
from Sprites_Archive import floor_music, sfx
import os 

class Sound_Manager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(sfx_channels)

        self.sfx_volume = sfx_default_volume
        self.music_volume = music_default_volume

        self.sounds = {}

        self.current_floor = None
        self.playlist = []
        self.track_index = 0
        self.track_playing = False
        self.track_timer = 0
        self.gap_left = 0

        self.track_length = 0

        self._load_sounds()

    def _load_sounds(self):
        for name, path in sfx.items():
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(self.sfx_volume)
                self.sounds[name] = snd
            except Exception as e:
                print(f"[Sound_Manager] Не загружен SFX '{name}': {e}")
                self.sounds[name] = None

    def play(self, name, volume=1):
        snd = self.sounds.get(name)
        if snd is None:
            return
        channel = pygame.mixer.find_channel()
        if channel is None:
            return
        channel.set_volume(self.sfx_volume * volume)
        channel.play(snd)

    def set_floor_music(self, floor):
        if floor == self.current_floor:
            return
        self.current_floor = floor
        self.playlist = list(floor_music.get(floor, []))
        self.track_index = 0
        self.track_playing = False
        self.gap_left = 0
        self.track_timer = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(self.music_volume)
        if self.playlist:
            self._start_current_track()

    def _start_current_track(self):
        if not self.playlist:
            return
        path = self.playlist[self.track_index]
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(0, fade_ms=music_fade_in_ms)
            self.track_playing = True
            self.track_timer = 0
            self.track_length = pygame.mixer.Sound(path).get_length()
        except Exception as e:
            print(f"[Sound_Manager] Не загружена музыка '{path}': {e}")
            self.track_playing = False
            self.track_length = 0

    def update(self, dt):
        if not self.playlist:
            return
        if self.track_playing:
            self.track_timer += dt
            if not pygame.mixer.music.get_busy():
                self.track_playing = False
                pygame.mixer.music.fadeout(music_fade_out_ms)
                self.gap_left = music_gap_sec
                return
            if self.track_length > 0 and self.track_timer >= self.track_length - (music_fade_out_ms / 1000):
                pygame.mixer.music.fadeout(music_fade_out_ms)
                self.track_playing = False
                self.gap_left = music_gap_sec
        elif self.gap_left > 0:
            self.gap_left = max(0, self.gap_left - dt)
            if self.gap_left == 0:
                self.track_index += 1
                if self.track_index >= len(self.playlist):
                    self.track_index = 0
                self._start_current_track()

    def stop_music(self, fade_ms=None):
        pygame.mixer.music.fadeout(fade_ms if fade_ms is not None else music_fade_out_ms)
        self.track_playing = False
        self.gap_left = 0

    def set_sfx_volume(self, v):
        self.sfx_volume = max(0, min(1, v))
        for snd in self.sounds.values():
            if snd is not None:
                snd.set_volume(self.sfx_volume)

    def set_music_volume(self, v):
        self.music_volume = max(0, min(1, v))
        pygame.mixer.music.set_volume(self.music_volume)

    def change_sfx_volume(self, delta):
        self.set_sfx_volume(self.sfx_volume + delta)

    def change_music_volume(self, delta):
        self.set_music_volume(self.music_volume + delta)

    def play_death_music(self):                                   
        self.stop_music()
        try:
            pygame.mixer.music.load("Assets/Music/Artega Tower Death.mp3")
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(0)
        except Exception as e:
            print("[Sound_Manager] Не загружена музыка смерти")

    def stop_death_music(self):                                   
        pygame.mixer.music.fadeout(music_fade_out_ms)
        self.track_playing = False
        self.gap_left = 0