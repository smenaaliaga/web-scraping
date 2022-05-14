text = "https://maps.googleapis.com/maps/api/staticmap?client=gme-mercadolibre&maptype=roadmap&scale=2&format=jpg&center=-33.4517691%2C-70.6493484&zoom=16&size=732x300&signature=cayzG_JvwKF9_CR5I9OpvrasKKE= 2x"

array = text.split('center=')
array = array[1].split('&zoom')
array = array[0].split('%2C')

print(array[1])