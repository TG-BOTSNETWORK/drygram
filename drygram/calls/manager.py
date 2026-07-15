# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from typing import Optional, List, Callable, Any

class CallParticipant:
    def __init__(self, user_id: int, muted: bool = False, video: bool = False, speaking: bool = False):
        self.user_id = user_id
        self.muted = muted
        self.video = video
        self.speaking = speaking

class CallManager:
    def __init__(self):
        self.active_calls = {}
        self.participants = {}
        self.volume = 100
        self.muted = False
        self.playing = False
        self.queue = []
        self.playlist = []
        self.current_track = None
        self.is_recording = False
        self.recording_file = None
        self.participant_callbacks = []
        self.video_quality = "720p"
        self.screen_sharing = False
        self.adaptive_streaming = True
        self.speaker_callbacks = []

    async def enter_room(self, chat_id: int) -> None:
        self.active_calls[chat_id] = True
        self.participants[chat_id] = []
        self.playing = True

    async def exit_room(self, chat_id: int) -> None:
        if chat_id in self.active_calls:
            del self.active_calls[chat_id]
        if chat_id in self.participants:
            del self.participants[chat_id]
        self.playing = False
        self.current_track = None
        self.queue.clear()
        self.screen_sharing = False

    async def stream_audio(self, chat_id: int, source: str) -> None:
        self.playing = True
        self.current_track = source

    async def stream_video(self, chat_id: int, source: str, quality: str = "720p") -> None:
        self.playing = True
        self.current_track = source
        self.video_quality = quality

    async def pause(self, chat_id: int) -> None:
        self.playing = False

    async def resume(self, chat_id: int) -> None:
        self.playing = True

    async def seek(self, chat_id: int, seconds: int) -> None:
        pass

    async def add_to_queue(self, source: str) -> None:
        self.queue.append(source)

    async def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(200, volume))

    async def mute(self) -> None:
        self.muted = True

    async def unmute(self) -> None:
        self.muted = False

    async def start_recording(self, file_path: str) -> None:
        self.is_recording = True
        self.recording_file = file_path

    async def stop_recording(self) -> None:
        self.is_recording = False
        self.recording_file = None

    async def start_screen_share(self, chat_id: int) -> None:
        self.screen_sharing = True

    async def stop_screen_share(self, chat_id: int) -> None:
        self.screen_sharing = False

    async def set_video_quality(self, quality: str) -> None:
        self.video_quality = quality

    async def toggle_adaptive_streaming(self, enabled: bool) -> None:
        self.adaptive_streaming = enabled

    def on_participant_event(self, callback: Callable[[CallParticipant], Any]) -> None:
        self.participant_callbacks.append(callback)

    def on_speaker_detection(self, callback: Callable[[List[int]], Any]) -> None:
        self.speaker_callbacks.append(callback)

    async def trigger_participant_event(self, participant: CallParticipant) -> None:
        for cb in self.participant_callbacks:
            try:
                cb(participant)
            except Exception:
                pass

    async def trigger_speaker_detection(self, speaking_user_ids: List[int]) -> None:
        for cb in self.speaker_callbacks:
            try:
                cb(speaking_user_ids)
            except Exception:
                pass
