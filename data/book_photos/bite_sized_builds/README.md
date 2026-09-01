# Bite-Sized Builds — Photo Drop Folder

Drop book page photos here. Each build can be one or more images (overview + steps).

## Naming (optional but helpful)

```
01_fishing_hut.jpg
02_watchtower.jpg
03_treehouse.jpg
```

## What happens next

For each photo batch, the pipeline adds:

1. Registry entry (`bite_*` id) with caption and palette
2. Procedural voxel generator (training data)
3. `.litematic` via `generate_book_builds`
4. Inclusion in preprocess → training `.npz`

You can also send photos in chat — same process.

## Status

See `manifest.json` for which builds are done vs pending.
