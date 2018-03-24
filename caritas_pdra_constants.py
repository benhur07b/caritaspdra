# COLOR SCHEME
RISK_COLORS = [("LOW", "green", "LOW"),
               ("MEDIUM", "orange", "MEDIUM"),
               ("HIGH", "red", "HIGH")]

RISK_COLORS_INV = [("LOW", "red", "LOW"),
                   ("MEDIUM", "orange", "MEDIUM"),
                   ("HIGH", "green", "HIGH")]

COUNT_HH_COLORS = [(0, 0, 'white', "0 households"),
                   (1, 3, 'cyan', "1 - 3 households"),
                   (4, 6, 'green', "4 - 6 households"),
                   (7, 9, 'orange', "7 - 9 households"),
                   (10, 9999999, 'red', "> 10 households")]

COUNT_PP_COLORS = [(0, 0, 'white', "0 persons"),
                   (1, 3, 'cyan', "1 - 3 persons"),
                   (4, 6, 'green', "4 - 6 persons"),
                   (7, 9, 'orange', "7 - 9 persons"),
                   (10, 9999999, 'red', "> 10 persons")]

PERCENTAGE_COLORS = [(0, 0, 'white', "0%"),
                     (1, 25, 'cyan', "1% - 25%"),
                     (26, 50, 'green', "26% - 50%"),
                     (51, 75, 'orange', "51% - 75%"),
                     (75, 100, 'red', "76% - 100%")]
