# Relic Picker Flow

When a battle ends, the backend rolls for a relic drop. Normal fights grant a relic 10% of the time, while boss rooms roll at 50%. If a relic is awarded, its star rank is determined by the encounter type and three relic options of that rank are returned to the frontend.

The frontend displays these options in the reward overlay using the same star-color tinting as cards. Selecting a relic posts the choice to `/relics/<run_id>`; the backend saves the relic to the run and only allows advancing rooms once all reward selections are complete.
