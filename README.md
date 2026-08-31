# Ogden Bike Bus

Static site for the Ogden Elementary bike bus, River North, Chicago.
Plain HTML and CSS — no build step, no dependencies.

## Put it on GitHub Pages

1. Create a new repository on GitHub (public), e.g. `bikeogden`.
2. Upload every file in this folder to the repo root. You can drag and drop
   them into the GitHub web uploader — no command line needed.
3. Go to **Settings → Pages**.
4. Under **Source**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`.
5. Save. After a minute the site is live at
   `https://YOUR-USERNAME.github.io/bikeogden/`.

### Using a custom domain (optional)

Buy a domain, then in **Settings → Pages → Custom domain** enter it and follow
GitHub's DNS instructions. GitHub will add a `CNAME` file to the repo for you.

## Editing

Every page is a plain `.html` file you can edit directly on GitHub: open the
file, click the pencil icon, change the text, commit. The site rebuilds in
about a minute.

The text you'll change most often:

| What | Where |
| --- | --- |
| Ride times and stops | `route.html` (and `espanol.html`) |
| Big ride dates | `calendar.html` |
| First-timer info and rules | `faq.html` |
| Photos from rides | `past-events.html` |
| Printable flyers | `flyers.html` |

## Images

Drop image files into `assets/`.

Photos currently in use:

| File | Where | Shows |
| --- | --- | --- |
| `hero.jpg` | homepage | riders in the green protected lane |
| `route-lane.jpg` | route | protected lane alongside traffic |
| `faq-group.jpg` | FAQs | the group waiting at a crossing |
| `about-racks.jpg` | about | bikes locked at the school racks |
| `past-crossing.jpg` | past events | the group at an intersection |
| `past-gathering.jpg` | past events | gathering before roll-out |
| `past-group.jpg` | past events | a full bus waiting to cross |
| `owl.svg` | masthead, homepage, favicon | the Ogden owl in a helmet |
| `route-map-jenner.svg` | route | the Ogden-to-Jenner continuation |
| `owl.svg` | every page header, homepage | the owl mark |
| `route-map-jenner.svg` | route | proposed continuation to Jenner |

`hero.svg` is an illustrated alternative — change the `src` in `index.html` to
`assets/hero.svg` to use it instead.

To add a photo: drop the file in `assets/`, resize it to about 1400px wide and
under 350 KB, then copy an existing `<figure>` block and change the filename,
the `alt` text, and the caption.

**On faces:** the photos here show riders from behind or with faces redacted.
If you add a photo where children are identifiable, either redact the faces the
way you did on the crossing photo, or check with those families first.

Aim for images under about 500 KB so the site stays fast on phones.

## Things to fill in

- Real ride times if the approximate ones are wrong
- October and May national ride dates once announced
- A hero photo and a route map
- Flyer PDFs

## The route map

The route page uses a drawn map, `assets/route-map.svg`. It's a plain text file
you can open in any editor — no Google Maps dragging required. To change it:

- **Stop times** — search for `8:00`, `8:05` and edit the text.
- **Street names** — search for `Orleans`, `Wells`, `Dearborn` and edit.
- **The route line** — the `<polyline points="...">` near the top. Points are
  `x,y` pairs.

The grid is drawn to the real Chicago address system, where 2 units on the map
equals 1 address number:

| Street | Coordinate |
| --- | --- |
| Kingsbury (angled) | x = 200 at Illinois, 120 at Erie |
| Orleans (340W) | x = 320 |
| Wells (200W) | x = 600 |
| Dearborn (40W) | x = 920 |
| State (0) | x = 1000 |
| Walton (932N) | y = 56 |
| Chicago Ave (800N) | y = 320 |
| Erie (658N) | y = 604 |
| Ohio (600N) | y = 720 |
| Illinois (500N) | y = 920 |

So to move a stop one block, work out the address difference and double it.
Because it's vector it stays sharp at any size and prints cleanly on flyers.

### The Jenner continuation

`assets/route-map-jenner.svg` shows the 8:30 leg from Ogden to the Jenner
campus. Its grid uses the same 2-units-per-address-number scale, with Cleveland
at x=120, Hudson at x=240, Wells at x=720, Clark at x=920, Elm at y=42, Oak at
y=280, Walton at y=416 and Delaware at y=480.

The street west of Wells on this leg is Locust.

The route page also carries a short "we're still tweaking the route" note above
the map. Once the route is settled, delete that `<div class="note">` block in
both files.

## The Jenner continuation

The route page describes a continuation from Ogden to the Jenner campus
(1119 N Cleveland), leaving 8:30 and arriving 8:40. It is written as a proposal
that starts when a family asks for it, so no names or numbers are claimed.
Once it's running, edit the three paragraphs under "Continuing to Jenner" in
`route.html` and the matching Spanish text in `espanol.html`.

One street on that route is unlabeled — the block heading west after Wells,
south of Oak. The map marks it "street name to confirm". Once you know it,
search `route-map-jenner.svg` for that phrase and replace it.

## The owl

`assets/owl.svg` is an original drawing, not the school's crest — safe to use
without permission. If Ogden has an official owl logo you're allowed to use,
save it over this file (square, and SVG or PNG with a transparent background).

## Embedding your Google Calendar

In Google Calendar: **Settings → your calendar → Integrate calendar → Embed code**.
Paste that `<iframe>` into `calendar.html` where the comment marks the spot.

## Updating an existing copy

If you already have this site on your computer with your own files added to
`assets/`, **do not replace the whole folder** — you'll lose them. Instead:

1. Copy the `.html` files, `README.md` and `.nojekyll` over the old ones.
2. Open the new `assets/` folder and copy its files into your existing one,
   choosing "merge" or "keep both" if asked. Your flyers stay put.

## A note on the archived flyers

Two 2024 PDFs and one 2025 image originally printed an organizer's personal
email address. Those have been redacted: the PDFs were flattened to images with
the contact line painted out, so no selectable text remains, and the line was
painted out of the JPEG.

If you add older material, check it for personal contact details before
committing — anything in this repo is public and gets crawled.

## Flyers

Thirteen flyers are already in `assets/` and linked from `flyers.html`, renamed
to lowercase with hyphens. Avoid spaces in filenames — a file called
`weekly bike bus Fridays.png` has to be written `weekly%20bike%20bus%20Fridays.png`
in a link, and it's easy to get wrong.

To add another: put the file in `assets/`, then copy a `<li>` line in
`flyers.html` and change the filename and the text.

Large images were compressed on the way in — the two big PNGs went from 3 MB
and 4 MB down to about 300 KB each. Anything over ~500 KB is worth shrinking
before adding, or the page crawls on phone data.

## Making QR codes

`tools/make-qr.py` generates a QR code as an SVG. Python only, no installs:

```
python3 tools/make-qr.py "https://your-url-here" assets/qr-name.svg
```

Add `L`, `M`, `Q` or `H` as a third argument to set error correction. `Q` is
the default and the right choice for print — it survives folding, rain and
being photographed at an angle. `H` is tougher still but makes a denser code.

Two are already generated, each as SVG (for print) and PNG (for tools that
won't take an SVG):

- `assets/qr-whatsapp.*` -> the WhatsApp group. Address-independent, so it keeps
  working even if the site moves. **This is the one to put on flyers.**
- `assets/qr-site.*` -> https://sondzus.github.io/BikeBusOgden/ . If you ever
  buy a domain or rename the repo, this one stops working and any printed copies
  are dead. Regenerate it after any URL change.
Because it encodes the WhatsApp invite rather than a website, it keeps working
no matter where the site is hosted.

Being SVG, it scales to any size without going fuzzy — drop it straight into a
flyer at whatever size you need. Print it at least 2 cm across, keep the white
margin around it, and don't put anything on top of it.

## Adding a calendar feed

`calendar.html` has a commented placeholder near the bottom marked
`CALENDAR FEED`. It explains where to get the embed code from Google Calendar
and where to paste it. A `.calendar-embed` wrapper class is already in the
stylesheet so the embed stays responsive on phones — the comment shows how to
use it. There's also a note on linking an iCal feed if you'd rather people
subscribe than look at a grid.

## Structure

```
index.html        Landing page — deliberately minimal
route.html        Stops and times
faq.html          What a bike bus is, rules, how to join
calendar.html     Ride days
about.html        Who we are
past-events.html  Photo archive
flyers.html       Printables
espanol.html      Spanish version
assets/style.css  All styling
.nojekyll         Tells GitHub Pages to serve files as-is
```

## Notes

The landing page is intentionally sparse: name, one line about when we ride,
a button to join WhatsApp, a photo. Everything else lives one click away.
Resist adding to it — it's the page a new parent sees first.
