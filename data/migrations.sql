CREATE TABLE "movimientos"(
    "id" INTEGER NOT NULL,
    "date" TEXT,
    "time" TEXT,
    "from_currency" INTEGER,
    "form_quantity" REAL,
    "to_currency" INTEGER,
    "to_quantity" REAL,
    "precio_unitario" REAL,
    PRIMARY KEY("id")
)

