# videoprojet

## Séparation voix / musique de fond

La piste audio de `videoplayback_2.mp4` (6 min 12 s, stéréo 44,1 kHz) a été
séparée en deux pistes avec [Demucs](https://github.com/facebookresearch/demucs)
(modèle `htdemucs_ft`, le plus précis de Demucs) :

| Fichier | Contenu |
| --- | --- |
| `sortie/musique_fond.flac` | Musique de fond seule, sans perte (à privilégier pour le montage) |
| `sortie/musique_fond.mp3` | Musique de fond seule, MP3 320 kb/s |
| `sortie/voix.flac` | Voix seule, sans perte |
| `sortie/voix.mp3` | Voix seule, MP3 320 kb/s |

Les deux pistes gardent exactement la durée et le calage de la vidéo
d'origine : on peut les replacer telles quelles sur la timeline.

Contrôles effectués :

- pas d'écrêtage (crête musique 0,74, voix 0,98) ;
- pas de fuite de voix notable dans la musique : dans la bande de la parole,
  la musique est environ 24 dB sous la voix, et son enveloppe ne suit pas
  celle de la voix.

### Refaire la séparation sur une autre vidéo

```bash
./separer_voix_musique.sh ma_video.mp4 sortie_ma_video
```

Les prérequis sont en tête du script. Sur un CPU 4 cœurs, comptez environ
10 minutes de calcul par minute d'audio.
