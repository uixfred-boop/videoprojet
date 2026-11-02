// Runs Shopify Theme Check on the theme root (one folder up) and prints offenses.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { check } from '@shopify/theme-check-node';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const offenses = await check(root);
const sev = ['ERROR', 'WARNING', 'INFO'];
const rel = (u) => decodeURIComponent(u).replace('file://' + root + '/', '');
offenses.sort((a, b) => a.severity - b.severity || rel(a.uri).localeCompare(rel(b.uri)));
for (const o of offenses) console.log(`${sev[o.severity] || o.severity}\t${o.check}\t${rel(o.uri)}:${(o.start?.line ?? 0) + 1}\t${o.message}`);
const errors = offenses.filter((o) => o.severity === 0).length;
console.log(`\n${offenses.length} offenses (${errors} errors)`);
process.exit(errors ? 1 : 0);
