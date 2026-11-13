from pathlib import Path

target = Path("EditAI/frontend/src/components/VideoPlayer.jsx")
text = target.read_text(encoding="utf-8")

old_vid = """          {activeClipSrc ? (
            <video
              ref={videoRef}
              src={activeClipSrc}
              onTimeUpdate={handleTimeUpdate}
              onEnded={handleVideoEnded}
              className="w-full h-full object-contain max-h-[58vh]"
              playsInline
            />"""

new_vid = """          {activeClipSrc ? (
            <video
              ref={videoRef}
              src={activeClipSrc}
              onTimeUpdate={handleTimeUpdate}
              onEnded={handleVideoEnded}
              style={{ filter: activeClip?.filter || 'none' }}
              className="w-full h-full object-contain max-h-[58vh] transition-[filter] duration-300"
              playsInline
            />"""

assert old_vid in text, "old_vid not found"
text = text.replace(old_vid, new_vid, 1)

old_sub = """          {/* Subtitle Overlay */}
          {activeSubtitle && (
            <div className="absolute bottom-5 left-1/2 -translate-x-1/2 max-w-[85%] text-center pointer-events-none z-10">
              <span className="inline-block px-2.5 py-1 rounded bg-black/85 text-[#f0f2f5] font-normal text-xs md:text-sm border border-white/15 shadow">
                {activeSubtitle}
              </span>
            </div>
          )}"""

new_sub = """          {/* Subtitle / Title Overlay */}
          {activeSubtitle && (
            <div className="absolute bottom-5 left-1/2 -translate-x-1/2 max-w-[85%] text-center pointer-events-none z-10">
              <span
                style={{
                  color: (subtitles || []).find((s) => currentTime >= s.start_time && currentTime <= s.end_time)?.color || '#f0f2f5'
                }}
                className="inline-block px-3 py-1.5 rounded bg-black/85 font-medium text-xs md:text-sm border border-white/15 shadow-lg tracking-wide"
              >
                {activeSubtitle}
              </span>
            </div>
          )}"""

assert old_sub in text, "old_sub not found"
text = text.replace(old_sub, new_sub, 1)

target.write_text(text, encoding="utf-8")
print("VideoPlayer.jsx filter & title overlay patched successfully!")

