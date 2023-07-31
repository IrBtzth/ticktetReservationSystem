class Config(object):
    POSTS_PER_PAGE = 10
    SECRET_KEY='Secreto'
    RECAPTCHA_PUBLIC_KEY = '6Ld9NqcmAAAAABDDCfW3YQOKO35HUQLvvv9qhQM2'
    RECAPTCHA_PRIVATE_KEY = '6Ld9NqcmAAAAAMUknnNbHVY52m0AkBWThqzliGfO'
    STRIPE_PUBLIC_KEY='pk_test_51NMD53JljMONOdDhISlHNfDoEj6JqTofgbDwVylD7rGLhdZnUlW3dUehVrn044LLCIh51e6zyN3rbNfcmNGQ067j00FpIO3LAC'
    STRIPE_SECRET_KEY='sk_test_51NMD53JljMONOdDhgNaT0hdB11LX5QUFBGDQjaR9fJn7inhGpftnZHNdr751sJgJAVEEUFndcKImtgIrN9ilXIU200OnQ3zz7D'
    


class ProdConfig(Config):
    SECRET_KEY = '\xcb\xd7\x8a.\x82\x9c1Lu\xf1&2\xf6i\xfa\x8e\xb1\xc9t^\xccW\xdbw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/betza/ticketReservationSystem/database.db'


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = '\xa8\xcc\xeaP+\xb3\xe8 |\xad\xdb\xea\xd0\xd4\xe8\xac\xee\xfaW\x072@O3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/betza/ticketReservationSystem/database.db'


