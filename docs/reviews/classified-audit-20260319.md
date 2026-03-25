# Classified Folder Audit

- Generated at: 2026-03-19T20:01:03
- Method: compare each file location under `classified/*/Artist/*` against current `classify_file` prediction.
- Note: This is a heuristic audit to surface questionable placements for manual confirmation.

## Summary

- singles: 68 flagged out of 840 files in Artist folders
- albums: 39 flagged out of 130 files in Artist folders

## Singles Artist Folder Review

- Total files reviewed: 840
- Questionable entries flagged: 68

### Flagged Folders (count)

- FictionalBand_7d720b: 11
- CosmicHarmonies: 5
- FictionalBand_94bfb7: 5
- FictionalBand_6bbb72: 4
- FictionalBand_4fd89f: 4
- FictionalBand_f8e762: 4
- FictionalBand_6146d0: 4
- FictionalBand_96a033: 3
- FictionalBand_0da3df: 3
- FictionalBand_37003c: 3
- FictionalBand_73a521: 2
- FictionalBand_c7bd66: 2
- FictionalBand_ade44e: 2
- FictionalBand_6f9412: 2
- FictionalBand_ce3bd1: 2
- Various: 2
- FictionalBand_088f00: 1
- FictionalBand_1087a0: 1
- FictionalBand_a25df8: 1
- FictionalBand_962289: 1
- FictionalBand_ffd489: 1
- FictionalBand_f11f1b: 1
- FictionalBand_38b13c: 1
- FictionalBand_4c8735: 1
- FictionalBand_be7649: 1
- FictionalBand_d733b8: 1

### Sample Questionable Entries

- `singles/Artist/CosmicHarmonies/FictionalBand - rock-song-0f1e3c.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/CosmicHarmonies/FictionalBand - rock-song-2f953e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/CosmicHarmonies/FictionalBand - rock-song-56484b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/CosmicHarmonies/FictionalBand - rock-song-1fcf15.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/CosmicHarmonies/FictionalBand - rock-song-861b2d.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_f5b7d8]
- `singles/Artist/FictionalBand_088f00/FictionalBand - rock-song-252319.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_1087a0/FictionalBand - rock-song-7aea2e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_73a521/FictionalBand - rock-song-d16369.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_73a521/FictionalBand - rock-song-fa35d1.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6bbb72/FictionalBand - rock-song-1796d2.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6bbb72/FictionalBand - rock-song-51ba2b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6bbb72/FictionalBand - rock-song-3c3062.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6bbb72/FictionalBand - rock-song-d20255.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_a25df8/FictionalBand - rock-song-1bdc66.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_94bfb7/FictionalBand - rock-song-a4cb37.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_94bfb7/FictionalBand - rock-song-9258c4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a415ff]
- `singles/Artist/FictionalBand_94bfb7/FictionalBand - rock-song-8f4f3b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_94bfb7/FictionalBand - rock-song-e24ecc.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_94bfb7/FictionalBand - rock-song-7efb44.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [CosmicHarmonies]
- `singles/Artist/FictionalBand_c7bd66/FictionalBand - rock-song-fc136b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_d733b8]
- `singles/Artist/FictionalBand_c7bd66/FictionalBand - rock-song-714325.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_f5b7d8, FictionalBand_d733b8]
- `singles/Artist/FictionalBand_962289/FictionalBand - rock-song-b0b88c.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_ffd489/FictionalBand - rock-song-7d7f4d.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_4c8735]
- `singles/Artist/FictionalBand_4fd89f/FictionalBand - rock-song-4c4854.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_4fd89f/FictionalBand - rock-song-c56389.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_4fd89f/FictionalBand - rock-song-ed7184.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_4fd89f/FictionalBand - rock-song-75d8eb.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_f11f1b/FictionalBand - rock-song-1dfa6e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_38b13c/FictionalBand - rock-song-2fa6ab.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_ade44e/FictionalBand - rock-song-d49598.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_ade44e/FictionalBand - rock-song-b7fc0c.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_4c8735/FictionalBand - rock-song-8b56a0.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_96a033/FictionalBand - rock-song-9311c4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_96a033/FictionalBand - rock-song-0ef874.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_96a033/FictionalBand - rock-song-08285f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_0da3df/FictionalBand - rock-song-97b44e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_0da3df/FictionalBand - rock-song-d2804f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_0da3df/FictionalBand - rock-song-06139e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_f8e762/FictionalBand - rock-song-a36af5.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_f8e762/FictionalBand - rock-song-174b53.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_f8e762/FictionalBand - rock-song-025530.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_f8e762/FictionalBand - rock-song-7c1275.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-a92b92.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-f44e93.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-4a7a6e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-92009b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-b3192e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-cc2b14.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-cd165f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-9b2866.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-6aa92b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba, FictionalBand_f5b7d8]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-1680e5.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_82f6ba]
- `singles/Artist/FictionalBand_7d720b/FictionalBand - rock-song-2e91b0.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6f9412/FictionalBand - rock-song-5bcf00.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_6f9412/FictionalBand - rock-song-6b1e17.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_be7649/FictionalBand - rock-song-818fdb.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_d733b8/FictionalBand - rock-song-b9221b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_ce3bd1/FictionalBand - rock-song-ccb97a.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_ce3bd1/FictionalBand - rock-song-5825cd.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/Various/FictionalBand - rock-song-431346.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_7aeb94, FictionalBand_42d5d5]
- `singles/Artist/Various/FictionalBand - rock-song-5c1a4f.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_24ba5a]
- `singles/Artist/FictionalBand_37003c/FictionalBand - rock-song-0d4c27.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `singles/Artist/FictionalBand_37003c/FictionalBand - rock-song-e7d3d1.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_4c8735]
- `singles/Artist/FictionalBand_37003c/FictionalBand - rock-song-380e26.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_ffd489]
- `singles/Artist/FictionalBand_6146d0/FictionalBand - rock-song-87cd31.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a25df8]
- `singles/Artist/FictionalBand_6146d0/FictionalBand - rock-song-a805cf.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a25df8]
- `singles/Artist/FictionalBand_6146d0/FictionalBand - rock-song-8b8d0b.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a415ff]
- `singles/Artist/FictionalBand_6146d0/FictionalBand - rock-song-1ce0d4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a415ff]

## Albums Artist Folder Review

- Total files reviewed: 130
- Questionable entries flagged: 39

### Flagged Folders (count)

- MockCompany_Nintendo: 7
- CyberpunkBeats: 4
- Various: 4
- EgyptianMetal: 3
- FictionalBand_4cd56b: 3
- MockDJ_Nujabes: 2
- PirateMetal: 2
- DarkAngelMetal: 1
- Genesis: 1
- Journey: 1
- LsJack: 1
- MedievalAmbience: 1
- NeYo: 1
- NuMetalPlaylist: 1
- PhilCollins: 1
- FictionalBand_97c8f6: 1
- FictionalBand_2c2d2c: 1
- SamSmith: 1
- Scorpions: 1
- SummerEletrohits: 1
- FictionalBand_93cba0: 1

### Sample Questionable Entries

- `albums/Artist/CyberpunkBeats/FictionalBand - rock-song-cbf666.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/CyberpunkBeats/FictionalBand - rock-song-deeb0a.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/CyberpunkBeats/FictionalBand - rock-song-a069d4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/CyberpunkBeats/FictionalBand - rock-song-964846.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/DarkAngelMetal/FictionalBand - rock-song-2c650e.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/EgyptianMetal/FictionalBand - rock-song-dcd6dc.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/EgyptianMetal/FictionalBand - rock-song-20be12.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/EgyptianMetal/FictionalBand - rock-song-9b2e02.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/Genesis/FictionalBand - rock-song-63d114.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/Journey/FictionalBand - rock-song-880861.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/LsJack/FictionalBand - rock-song-14f913.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MedievalAmbience/FictionalBand - rock-song-ab54ea.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/NeYo/FictionalBand - rock-song-b5e0c2.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-7a413f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_f5b7d8]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-dd0af0.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-3ccf76.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-ad721f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-7e8254.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-e634c5.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockCompany_Nintendo/FictionalBand - rock-song-f8886c.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/NuMetalPlaylist/FictionalBand - rock-song-b86f80.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [FictionalBand_a415ff, FictionalBand_ce3bd1]
- `albums/Artist/MockDJ_Nujabes/FictionalBand - rock-song-e07e37.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/MockDJ_Nujabes/FictionalBand - rock-song-9a6bc4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/PhilCollins/FictionalBand - rock-song-f1cfe3.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/FictionalBand_4cd56b/FictionalBand - rock-song-d0f897.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/FictionalBand_4cd56b/FictionalBand - rock-song-356e27.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/FictionalBand_4cd56b/FictionalBand - rock-song-93059f.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/PirateMetal/FictionalBand - rock-song-96c772.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/PirateMetal/FictionalBand - rock-song-e49913.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/FictionalBand_97c8f6/FictionalBand - rock-song-b82919.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/FictionalBand_2c2d2c/FictionalBand - rock-song-9093fd.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/SamSmith/FictionalBand - rock-song-9231c4.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/Scorpions/FictionalBand - rock-song-9c7b0d.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/SummerEletrohits/FictionalBand - rock-song-259dcf.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
- `albums/Artist/Various/FictionalBand - rock-song-becf7e.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_c7bd66, FictionalBand_f5b7d8]
- `albums/Artist/Various/FictionalBand - rock-song-e35a80.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_f5b7d8]
- `albums/Artist/Various/FictionalBand - rock-song-e6b180.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_ce3bd1]
- `albums/Artist/Various/FictionalBand - rock-song-1b27e5.mp3`
  Reason: In Various but classifier suggests specific artist; predicted: [FictionalBand_ce3bd1]
- `albums/Artist/FictionalBand_93cba0/FictionalBand - rock-song-ee140c.mp3`
  Reason: Folder artist not present in classifier prediction; predicted: [Various]
