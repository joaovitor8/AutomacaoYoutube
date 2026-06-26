LINKS_E_FIXO = """
----------

Welcome to Astronautium 🚀✨, your portal to the soundscapes of the infinite universe, where stars, black holes, and alien civilizations collide in deep cosmic melodies. 🌌🌠

Journey through nebulae 🌈, interstellar abysses ⚫, distant planets 🌍, and other celestial bodies with my original instrumental compositions, created to evoke the mystery and grandeur of outer space. Each track is a sonic exploration of futuristic technologies, artificial intelligence, and invisible cosmic forces, a true musical odyssey into the unknown.

📌 New music and videos released regularly. Subscribe and activate the bell 🔔 to never miss a sonic journey through the cosmos.

Join the community of stellar explorers and share your experiences and emotions through musical spacetime. 🚀🌟

LINKS:
Subscribe to the channel: https://www.youtube.com/@Astronautium
Twitter: https://x.com/AstronautJonnes

✨ Thank you for being part of this sonic odyssey. Your support keeps this universe expanding and helps create new musical constellations for all of us.
"""

TAGS_FIXAS = [
  "SciFiMusic",
  "SpaceAmbient",
  "CosmicJourney",
  "InstrumentalSciFi",
  "SpaceMusic",
  "Astronaut",
]

def montar_descricao(frase_do_video: str, tags_do_video: list) -> str:
  todas_tags = TAGS_FIXAS + tags_do_video
  hashtags = ", ".join(f"#{tag}" for tag in todas_tags)

  descricao = f"{frase_do_video}\n{LINKS_E_FIXO}\n{hashtags}"
  return descricao

def montar_tags(tags_do_video: list) -> list:
  return TAGS_FIXAS + tags_do_video
