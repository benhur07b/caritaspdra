# COLOR SCHEME

RISK_COLORS = [("LOW", "green", "LOW"),
               ("MEDIUM", "orange", "MEDIUM"),
               ("HIGH", "red", "HIGH")]

RISK_COLORS_INV = [("LOW", "red", "LOW"),
                   ("MEDIUM", "orange", "MEDIUM"),
                   ("HIGH", "green", "HIGH")]

HH_0 = 0
HH_1 = 25
HH_2 = 50
HH_3 = 100

COUNT_HH_COLORS = [(0, 0, 'white', "0 households"),
                   (HH_0 + 1, HH_1, 'cyan', "{} - {} households".format(HH_0 + 1, HH_1)),
                   (HH_1 + 1, HH_2, 'green', "{} - {} households".format(HH_1 + 1, HH_2)),
                   (HH_2 + 1, HH_3, 'green', "{} - {} households".format(HH_2 + 1, HH_3)),
                   (HH_3 + 1, 9999999, 'red', "> {} households".format(HH_3 + 1))]

PP_0 = 0
PP_1 = 25
PP_2 = 50
PP_3 = 100

COUNT_PP_COLORS = [(0, 0, 'white', "0 households"),
                   (PP_0 + 1, PP_1, 'cyan', "{} - {} households".format(PP_0 + 1, PP_1)),
                   (PP_1 + 1, PP_2, 'green', "{} - {} households".format(PP_1 + 1, PP_2)),
                   (PP_2 + 1, PP_3, 'green', "{} - {} households".format(PP_2 + 1, PP_3)),
                   (PP_3 + 1, 9999999, 'red', "> {} households".format(PP_3 + 1))]


PERCENTAGE_COLORS = [(0, 0, 'white', "0%"),
                     (1, 25, 'cyan', "1% - 25%"),
                     (26, 50, 'green', "26% - 50%"),
                     (51, 75, 'orange', "51% - 75%"),
                     (75, 100, 'red', "76% - 100%")]
