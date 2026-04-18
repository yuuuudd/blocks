# Audio Asset Guide

## Directory Layout

- `Assets/Audio/`: legacy and manually imported assets.
- `Assets/Audio/Generated/`: generated SFX and short loops (recommended default location).

## Naming Convention

Use lowercase snake_case with stable event tags.

Pattern:

`<type>_<event>_<variant>.<ext>`

Examples:

- `sfx_move_tap_v1.ogg`
- `sfx_land_thump_v1.ogg`
- `sfx_clear_4_blast_v1.ogg`
- `bgm_menu_loop_v1.ogg`

## Recommended Extensions

- SFX: `ogg` first, `mp3` fallback.
- BGM: `ogg` + `mp3` dual export for compatibility.

## Event To File Mapping (v3.0)

| Event Key | Target File Path | Notes |
|---|---|---|
| piece_move | `Assets/Audio/Generated/sfx_move_tap_v1.wav` | 440Hz square, 50ms |
| piece_land | `Assets/Audio/Generated/sfx_land_thump_v1.wav` | 80Hz sine, 150ms |
| piece_rotate | `Assets/Audio/Generated/sfx_rotate_swish_v1.wav` | white noise + band-pass |
| wok_flip_start | `Assets/Audio/Generated/sfx_flip_rise_v1.wav` | 200->600Hz up sweep |
| wok_flip_end | `Assets/Audio/Generated/sfx_flip_clack_v1.wav` | 100Hz square + noise |
| clear_1 | `Assets/Audio/Generated/sfx_clear_1_ping_v1.wav` | 880Hz sine |
| clear_2 | `Assets/Audio/Generated/sfx_clear_2_pump_v1.wav` | dual 60Hz pulses |
| clear_3 | `Assets/Audio/Generated/sfx_clear_3_bass_v1.wav` | 40Hz saw + harmonics |
| clear_4 | `Assets/Audio/Generated/sfx_clear_4_blast_v1.wav` | noise + full-band sweep |
| level_clear | `Assets/Audio/Generated/sfx_level_clear_arp_v1.wav` | C-E-G arpeggio |
| game_over | `Assets/Audio/Generated/sfx_game_over_low_v1.wav` | 60Hz fade out |
| cat_trigger | `Assets/Audio/Generated/sfx_cat_meow_v1.wav` | 500->300Hz glide |

## Existing Imported Files

Current files in `Assets/Audio/`:

- `Main.mp3`
- `Enum.mp3`
- `Collide.mp3`
- `Wall.mp3`

If a file should join the managed pipeline, copy or rename it into `Assets/Audio/Generated/` using the convention above.
