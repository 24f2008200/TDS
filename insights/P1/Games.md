Great question! Here's the full solution condensed with explanations:

---

## What We Did (The Full Flow)

### 1. Recon — Understand the game state
```javascript
// Always start by knowing where you are and what you have
fetch('/signal/look', { headers: { 'X-Session-Token': TOKEN } })
fetch('/signal/inventory', { headers: { 'X-Session-Token': TOKEN } })
```
**Lesson:** Before acting, gather information first.

---

### 2. Get Hints — Don't brute force
```javascript
fetch('/signal/hint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Session-Token': TOKEN },
  body: JSON.stringify({ puzzle: 'PUZZLE_2_FREQUENCY' })
})
// Hint said: "statistical center of all candidates"
// = MEDIAN of the frequency list
```
**Lesson:** Hints tell you the *algorithm*, not the answer. Read them carefully.

---

### 3. Puzzle 2 — Median Frequency
```javascript
const frequencies = [91.8, 101.5, 95.6, 89.7, 101.0, 107.5, 87.9, 
                     91.2, 92.6, 99.6, 97.3, 102.0, 102.9, 99.8, 89.1];
const sorted = frequencies.sort((a, b) => a - b);
const median = sorted[Math.floor(sorted.length / 2)]; // → 97.3
```
**Lesson:** "Statistical center" = **median**. Sort the list, pick the middle value.

---

### 4. Puzzle 1 — PIN from clues
```javascript
// INSPECTION_CERTIFICATE said: Inspection date: 2021
// NOTEBOOK said: "PIN = inspection year + sublevel number"
// NOTEBOOK had: floor number 2 circled
const PIN = 2021 + 2; // → 2023
```
**Lesson:** Clues are spread across multiple items. **Cross-reference** them.

---

### 5. Craft POWERED_TUNER — Item combining
```javascript
// FREQUENCY_TUNER had "dead display, detachable power port"
// POWER_CELL was in POWER_ROOM
// Combine them → POWERED_TUNER
fetch('/signal/combine', {
  body: JSON.stringify({ item_a: 'FREQUENCY_TUNER', item_b: 'POWER_CELL' })
})
```
**Lesson:** Item descriptions are hints. "Dead display + power port" → needs a power source.

---

### 6. Navigate systematically
```javascript
// Map adjacency matters — you can't teleport
// ENT → SRA → MAI → PWR  (to get POWER_CELL)
// MAI → CTL → ARC        (to reach TERMINAL_3)
for (let room of ['ENTRANCE_HALL', 'SERVER_ROOM_A', 'MAINTENANCE_BAY', 'POWER_ROOM']) {
  await fetch('/signal/move', { body: JSON.stringify({ to: room }) })
}
```
**Lesson:** Draw or read the map first. Plan your **route** before moving.

---

### 7. Assemble the passcode
```javascript
// Fragment 1 (PIN_TERMINAL)    → WZV2
// Fragment 2 (RADIO_TRANSMITTER) → KQDH  
// Fragment 3 (TERMINAL_3)      → SD92
const passcode = 'WZV2' + 'KQDH' + 'SD92'; // → WZV2KQDHSD92
```
**Lesson:** The game told you upfront — "concatenate fragments in order revealed."

---

## The Big Lessons

| What we did | Real-world skill |
|---|---|
| Read hints before guessing | Read documentation before coding |
| Scanned all rooms for items | Explore the full API/codebase first |
| Used browser console to call APIs directly | API testing (like Postman/curl) |
| Decoded the JWT completion token | Understanding JWT structure |
| Sequential async/await navigation | Handling dependent async operations |

The biggest one: **the game's client-side code told us everything** — all the endpoints, request formats, and data structures were readable in the HTML source. Always read the source! 🔍
