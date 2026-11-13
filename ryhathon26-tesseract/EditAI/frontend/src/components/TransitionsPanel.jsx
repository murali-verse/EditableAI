import React, { useState } from 'react';
import {
  Scissors,
  Sparkles,
  CheckCircle2,
  Sliders,
  Layers,
  ArrowRightLeft,
  Zap,
  Eye,
  Film
} from 'lucide-react';

const TRANSITION_PRESETS = [
  {
    id: 'cross_dissolve',
    name: 'Cross Dissolve',
    category: 'Dissolve',
    description: 'Classic smooth blend between video clips',
    duration: 1.0,
    icon: '✨',
    color: '#3b82d4'
  },
  {
    id: 'dip_to_black',
    name: 'Dip to Black',
    category: 'Dissolve',
    description: 'Fades down to complete black then into the next clip',
    duration: 1.0,
    icon: '🌑',
    color: '#1a1a1a'
  },
  {
    id: 'dip_to_white',
    name: 'Dip to White',
    category: 'Dissolve',
    description: 'Flash-frame white transition for dramatic impact',
    duration: 0.6,
    icon: '⚪',
    color: '#e2e8f0'
  },
  {
    id: 'whip_pan_left',
    name: 'Whip Pan Left',
    category: 'Kinetic',
    description: 'High-speed directional camera whip pan to the left',
    duration: 0.5,
    icon: '⏩',
    color: '#d48b3b'
  },
  {
    id: 'smooth_zoom_in',
    name: 'Smooth Zoom In',
    category: 'Kinetic',
    description: 'Punch-in cinematic push into the focal point',
    duration: 0.8,
    icon: '🔍',
    color: '#a855f7'
  },
  {
    id: 'blur_dissolve',
    name: 'Gaussian Blur Dissolve',
    category: 'Stylized',
    description: 'Soft defocuses out of cut 1 and refocuses into cut 2',
    duration: 1.0,
    icon: '🌫️',
    color: '#06b6d4'
  },
  {
    id: 'glitch_cut',
    name: 'Digital Glitch Cut',
    category: 'Stylized',
    description: 'Modern cyberpunk RGB displacement glitch transition',
    duration: 0.4,
    icon: '⚡',
    color: '#ec4899'
  },
  {
    id: 'radial_iris',
    name: 'Radial Iris Wipe',
    category: 'Wipe',
    description: 'Circular focal mask expanding outwards',
    duration: 1.0,
    icon: '⭕',
    color: '#10b981'
  }
];

export default function TransitionsPanel({
  timeline,
  onApplyTransition
}) {
  const [selectedId, setSelectedId] = useState('cross_dissolve');
  const [duration, setDuration] = useState(1.0);
  const [targetScope, setTargetScope] = useState('selected'); // 'selected' | 'all'
  const [appliedNotice, setAppliedNotice] = useState(null);

  const selectedPreset = TRANSITION_PRESETS.find((t) => t.id === selectedId) || TRANSITION_PRESETS[0];
  const clipCount = timeline?.clips?.length || 0;

  const handleApply = () => {
    if (onApplyTransition) {
      onApplyTransition({
        ...selectedPreset,
        duration,
        targetScope
      });
    }

    setAppliedNotice(`Applied "${selectedPreset.name}" (${duration}s) to ${targetScope === 'all' ? 'all cuts' : 'selected cut'}`);
    setTimeout(() => setAppliedNotice(null), 3000);
  };

  return (
    <div className="h-full flex flex-col bg-[#141518] text-[#a0a4ae] select-none text-[11px] overflow-hidden">
      {/* 1. Header */}
      <div className="h-8 px-3 border-b border-[#212328] flex items-center justify-between bg-[#18191d]">
        <div className="flex items-center gap-1.5 text-[#d0d3dc] font-medium">
          <ArrowRightLeft className="w-3.5 h-3.5 text-[#c084fc]" />
          <span>Video Transitions</span>
          <span className="text-[10px] text-[#636875] font-mono">
            ({TRANSITION_PRESETS.length} Presets)
          </span>
        </div>
      </div>

      {/* 2. Transition Settings Box */}
      <div className="p-2.5 border-b border-[#212328] bg-[#121316] space-y-2">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-[#888e9d] font-medium uppercase tracking-wider">Target Cuts</span>
          <div className="flex items-center gap-1 bg-[#18191e] p-0.5 rounded border border-[#23252b]">
            <button
              onClick={() => setTargetScope('selected')}
              className={`px-2 py-0.5 rounded text-[10px] transition ${
                targetScope === 'selected'
                  ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                  : 'text-[#6f7482] hover:text-[#c084fc]'
              }`}
            >
              Selected Clip
            </button>
            <button
              onClick={() => setTargetScope('all')}
              className={`px-2 py-0.5 rounded text-[10px] transition ${
                targetScope === 'all'
                  ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                  : 'text-[#6f7482] hover:text-[#c084fc]'
              }`}
            >
              All Cuts ({clipCount})
            </button>
          </div>
        </div>

        {/* Duration Slider */}
        <div className="space-y-1">
          <div className="flex justify-between text-[10px] text-[#888e9d]">
            <span>Transition Duration:</span>
            <span className="text-[#c4c7d2] font-mono">{duration.toFixed(1)}s</span>
          </div>
          <input
            type="range"
            min="0.2"
            max="3.0"
            step="0.1"
            value={duration}
            onChange={(e) => setDuration(parseFloat(e.target.value))}
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

      {/* 3. Transitions List */}
      <div className="flex-1 overflow-y-auto p-2.5 space-y-1.5">
        <span className="text-[10px] font-medium text-[#7a808e] block uppercase tracking-wider">
          Transition Library
        </span>
        <div className="space-y-1.5">
          {TRANSITION_PRESETS.map((preset) => {
            const isSelected = selectedId === preset.id;
            return (
              <div
                key={preset.id}
                onClick={() => {
                  setSelectedId(preset.id);
                  setDuration(preset.duration);
                }}
                className={`p-2 rounded border cursor-pointer transition flex items-start gap-2.5 ${
                  isSelected
                    ? 'bg-[#261c30] border-[#7c3aed] shadow-xs text-[#c084fc]'
                    : 'bg-[#17181c] hover:bg-[#1e2026] border-[#22242a]'
                }`}
              >
                <div className="w-7 h-7 rounded bg-[#101114] border border-[#25272e] flex items-center justify-center text-sm shrink-0">
                  {preset.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-[#d8dbe4] text-[11px] truncate">
                      {preset.name}
                    </span>
                    <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-[#101114] text-[#808696] border border-[#212328]">
                      {preset.category}
                    </span>
                  </div>
                  <p className="text-[10px] text-[#717684] line-clamp-1 mt-0.5">
                    {preset.description}
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
          Selected: <span className="text-[#c4c7d2] font-medium">{selectedPreset.name}</span>
        </div>
        <button
          onClick={handleApply}
          className="px-3 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] border border-[#7c3aed] text-[#c084fc] text-[10px] font-medium flex items-center gap-1.5 transition shadow-xs"
        >
          <Sparkles className="w-3 h-3 text-[#c084fc]" />
          <span>Apply Transition</span>
        </button>
      </div>
    </div>
  );
}

