import aschill_grafic as asc

source = 'images\kostf.jpg'
scale = 0.35

image = asc.get_image(source)

rw, rh = asc.get_sides_from_scale(image, scale)

# res1 = asc.algo1(image, rh, rw)
res2 = asc.algo1(image, rh, rw)

asc.to_pygame(res2, 'kostf4.png', font_size=16)
