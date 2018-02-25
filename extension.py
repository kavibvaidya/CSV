from zipline.data.bundles import register
from zipline.data.bundles.viacsv import viacsv

eqSym = {
    "AAPL",
    "GOOG",
    "INSY",
    "BND"
}

register(
    "csv",    # name this whatever you like, the bundle is then called using the same name
    viacsv(eqSym),
)
