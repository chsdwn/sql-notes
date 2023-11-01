def read_glados():
  # try:
  file = open("./glados-voice/1.mp3", "rb")
  return file.read()
  # except:
  #   print("except")
  #   pass
  # could not read file, return NULL
  # return None

read_glados()