// News-image entry for Thursday 26 November 2026 (Node 22, standard library only).
// The program copies the entry.png drawn for this day to the output
// directory, so the grader sees exactly the image this entry made.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
