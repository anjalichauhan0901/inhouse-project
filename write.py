import mfrc522
from os import uname


def do_write():
    if uname()[0] == "WiPy":
        rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == "esp8266":
        rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    print("")
    print("Place card before reader to write address 0x08")
    print("")

    try:
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print(
                        "  - uid	 : 0x%02x%02x%02x%02x"
                        % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    )
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            stat = rdr.write(
                                8,
                                b"\x55\x6e\x61\x75\x74\x68\x6f\x72\x69\x7a\x65\x64\x20\x20\x20\x20",
                            )
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("Data written to card")
                            else:
                                print("Failed to write data to card")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")

do_write()