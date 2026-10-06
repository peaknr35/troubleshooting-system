# frontend/app/compare -- the compare route

One job: the `/compare` page. One file.

## What's here
- `page.tsx` -- renders `<CompareView/>` in a wide container.

## Where things live
All compare logic is in `../../components/CompareView.tsx`; state is in
`../../contexts/ResearchContext.tsx` (`compareColumns`, `runCompare`). This folder
only wires the route.

## Links
- Parent: `../CONTEXT.md` . Component: `../../components/CompareView.tsx`
