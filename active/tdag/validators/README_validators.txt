TDAG Validator System

This directory contains all system-wide validation files for standardized references in generation and mechanics.
Each validator represents a canonical list of valid values used across simulation logic.

HOW TO USE:
- System files that use one of these validators should include a "validator_reference" field pointing to the appropriate file.
- Validators should be updated centrally — do NOT hardcode values inside generators or systems.

CURRENTLY LINKED:
- valid_elements.json
- valid_soul_colors.json
- valid_technique_qualities.json
- valid_body_ranks.json
- valid_soul_ranks.json
- valid_bloodline_tiers.json

READY BUT UNUSED:
- valid_pill_qualities.json
- valid_factions.json
- valid_city_tiers.json

To scan for references or missing validator integration, run a validator candidate scan across systems.

-- End of README --
