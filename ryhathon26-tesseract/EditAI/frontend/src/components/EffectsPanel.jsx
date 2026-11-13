import React, { useState } from 'react';
import {
  Sparkles,
  Sliders,
  CheckCircle2,
  Film,
  Zap,
  Volume2,
  Palette,
  Eye
} from 'lucide-react';

const EFFECT_PRESETS = [
  {
    id: 'teal_orange',
    name: 'Teal & Orange Blockbuster',
    category: 'Color LUT',
    description: 'Hollywood blockbuster color separation with rich skin tones',
    cssFilter: 'contrast(1.15) saturate(1.35) sepia(0.12) hue-rotate(-12deg)',
    badgeColor: '#38bdf8'
  },
  {
    id: 'golden_hour',
    name: 'Golden Hour Warmth',
    category: 'Color LUT',
    description: 'Soft sunlight glow with enhanced warm highlights',
    cssFilter: 'sepia(0.35) saturate(1.25) brightness(1.05)',
    badgeColor: '#fbbf24'
  },
  {
    id: 'monochrome_noir',
    name: 'Monochrome Noir 35mm',
    category: 'Color LUT',
    description: 'High-contrast cinematic black and white grade',
    cssFilter: 'grayscale(1.0) contrast(1.35) brightness(0.95)',
    badgeColor: '#94a3b8'
  },
  {
    id: 'cyberpunk_neon',
    name: 'Cyberpunk Neon',
    category: 'Stylized',
    description: 'Ultra-vibrant saturated shadows and electric highlights',
    cssFilter: 'saturate(1.8) contrast(1.25) hue-rotate(25deg)',
    badgeColor: '#c084fc'
  },
  {
    id: 'vintage_film',
    name: 'Vintage Kodak 1970s',
    category: 'Color LUT',
    description: 'Analog color fade with subtle warm highlights',
    cssFilter: 'sepia(0.25) contrast(0.95) brightness(1.08) saturate(1.1)',
    badgeColor: '#f97316'
  },
  {
    id: 'crisp_clarity',
    name: 'Sharpen & Enhance',
    category: 'Optics',
    description: 'Enhanced micro-contrast and edge clarity',
    cssFilter: 'contrast(1.25) brightness(1.02)',
    badgeColor: '#34d399'
  },
  {
    id: 'dreamy_glow',
    name: 'Dreamy Soft Glow',
    category: 'Optics',
    description: 'Ethereal diffused highlights and soft focus edges',
    cssFilter: 'brightness(1.12) blur(0.4px) contrast(0.95)',
    badgeColor: '#f472b6'
  },
  {
    id: 'audio_voice_boost',
    name: 'Voice Clarity EQ',
    category: 'Audio FX',
    description: 'Boosts vocal mid-range presence and speech intelligibility',
    isAudio: true,
    badgeColor: '#60a5fa'
  },
  {
    id: 'audio_denoiser',
    name: 'Studio De-Noiser',
    category: 'Audio FX',
    description: 'Attenuates background ambient hiss and room noise',
    isAudio: true,
    badgeColor: '#10b981'
  }
];

export default function EffectsPanel({
  selectedClip,
  timeline,
  onApplyEffect
}) {
  const [selectedEffectId, setSelectedEffectId] = useState('teal_orange');
  const [targetScope, setTargetScope] = useState('selected'); // 'selected' | 'all'
  const [intensity, setIntensity] = useState(100);
  const [appliedNotice, setAppliedNotice] = useState(null);

  const selectedPreset = EFFECT_PRESETS.find((e) => e.id === selectedEffectId) || EFFECT_PRESETS[0];

  const handleApply = () => {
    if (onApplyEffect) {
      onApplyEffect({
        ...selectedPreset,
        intensity: intensity / 100,
        targetScope
      });
    }

    setAppliedNotice(`Applied "${selectedPreset.name}" to ${targetScope === 'all' ? 'entire timeline' : (selectedClip ? selectedClip.name : 'selected clip')}`);
    setTimeout(() => setAppliedNotice(null), 3000);
  };

  return (
    <div className="h-full flex flex-col bg-[#141518] text-[#a0a4ae] select-none text-[11px] overflow-hidden">
      {/* 1. Header */}
      <div className="h-8 px-3 border-b border-[#212328] flex items-center justify-between bg-[#18191d]">
        <div className="flex items-center gap-1.5 text-[#d0d3dc] font-medium">
          <Sparkles className="w-3.5 h-3.5 text-[#c084fc]" />
          <span>Effects & Color LUTs</span>
          <span className="text-[10px] text-[#636875] font-mono">
            ({EFFECT_PRESETS.length} FX)
          </span>
        </div>
      </div>

      {/* 2. Target & Intensity Controls */}
      <div className="p-2.5 border-b border-[#212328] bg-[#121316] space-y-2">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-[#888e9d] font-medium uppercase tracking-wider">Target</span>
          <div className="flex items-center gap-1 bg-[#18191e] p-0.5 rounded border border-[#23252b]">
            <button
              onClick={() => setTargetScope('selected')}
              className={`px-2 py-0.5 rounded text-[10px] transition ${
                targetScope === 'selected'
                  ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                  : 'text-[#6f7482] hover:text-[#c084fc]'
              }`}
            >
              {selectedClip ? selectedClip.name?.slice(0, 10) + '...' : 'Selected Clip'}
            </button>
            <button
              onClick={() => setTargetScope('all')}
              className={`px-2 py-0.5 rounded text-[10px] transition ${
                targetScope === 'all'
                  ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                  : 'text-[#6f7482] hover:text-[#c084fc]'
              }`}
            >
              All Sequence
            </button>
          </div>
        </div>

        {/* Intensity Slider */}
        <div className="space-y-1">
          <div className="flex justify-between text-[10px] text-[#888e9d]">
            <span>Effect Intensity:</span>
            <span className="text-[#c4c7d2] font-mono">{intensity}%</span>
          </div>
          <input
            type="range"
            min="20"
            max="100"
            step="5"
            value={intensity}
            onChange={(e) => setIntensity(parseInt(e.target.value, 10))}
            className="w-full h-1 bg-[#23252c] rounded appearance-none accent-[#a855f7] cursor-pointer"
          />
        </div>

        {appliedNotice && (
          <div className="flex items-center gap-1.5 text-[10px] text-[#5bb676] bg-[#17241b] border border-[#223d2a] px-2 py-1 rounded">
            <CheckCircle2 className="w-3 h-3 shrink-0" />
            <span className="truncate">{appliedNotice}</span>
          </div>
        )}
      </div>

      {/* 3. Effects Presets List */}
      <div className="flex-1 overflow-y-auto p-2.5 space-y-1.5">
        <span className="text-[10px] font-medium text-[#7a808e] block uppercase tracking-wider">
          Effect Presets
        </span>
        <div className="space-y-1.5">
          {EFFECT_PRESETS.map((fx) => {
            const isSelected = selectedEffectId === fx.id;
            return (
              <div
                key={fx.id}
                onClick={() => setSelectedEffectId(fx.id)}
                className={`p-2 rounded border cursor-pointer transition flex items-start gap-2.5 ${
                  isSelected
                    ? 'bg-[#261c30] border-[#7c3aed] shadow-xs text-[#c084fc]'
                    : 'bg-[#17181c] hover:bg-[#1e1f26] border-[#22242a]'
                }`}
              >
                <div
                  style={{ borderColor: fx.badgeColor }}
                  className="w-7 h-7 rounded bg-[#101114] border flex items-center justify-center shrink-0"
                >
                  {fx.isAudio ? (
                    <Volume2 className="w-3.5 h-3.5" style={{ color: fx.badgeColor }} />
                  ) : (
                    <Palette className="w-3.5 h-3.5" style={{ color: fx.badgeColor }} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-[#d8dbe4] text-[11px] truncate">
                      {fx.name}
                    </span>
                    <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-[#101114] text-[#808696] border border-[#212328]">
                      {fx.category}
                    </span>
                  </div>
                  <p className="text-[10px] text-[#717684] line-clamp-1 mt-0.5">
                    {fx.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. Footer Apply Action */}
      <div className="p-2 border-t border-[#212328] bg-[#16171b] flex items-center justify-between">
        <div className="text-[10px] text-[#787d8c] truncate max-w-[170px]">
          Preset: <span className="text-[#c4c7d2] font-medium">{selectedPreset.name}</span>
        </div>
        <button
          onClick={handleApply}
          className="px-3 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] border border-[#7c3aed] text-[#c084fc] text-[10px] font-medium flex items-center gap-1.5 transition shadow-xs"
        >
          <Sparkles className="w-3 h-3 text-[#c084fc]" />
          <span>Apply Effect</span>
        </button>
      </div>
    </div>
  );
}

