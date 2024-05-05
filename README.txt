# RectanglesService

DB - postgres

Host: cornelius.db.elephantsql.com
Database - sfrfivyh
Username: sfrfivyh
Password: uT0xQahWmPQ8YD1ZOSmf7JSrDdz0dU7U
SSL: require

- SCHEMA:

CREATE TABLE Rectangles (
    RectangleId SERIAL PRIMARY KEY,
    CenterX DOUBLE PRECISION NOT NULL,
    CenterY DOUBLE PRECISION NOT NULL,
    Width DOUBLE PRECISION NOT NULL,
    Height DOUBLE PRECISION NOT NULL,
    Rotation DOUBLE PRECISION NOT NULL,
    PAx DOUBLE PRECISION,
    PAy DOUBLE PRECISION,
    PBx DOUBLE PRECISION,
    PBy DOUBLE PRECISION,
    PCx DOUBLE PRECISION,
    PCy DOUBLE PRECISION,
    PDx DOUBLE PRECISION,
    PDy DOUBLE PRECISION,
    MinX DOUBLE PRECISION,
    MaxX DOUBLE PRECISION,
    MinY DOUBLE PRECISION,
    MaxY DOUBLE PRECISION
);

CREATE OR REPLACE FUNCTION calculate_vertices_and_bounds()
RETURNS TRIGGER AS $$
DECLARE
    rad_angle DOUBLE PRECISION;
    cos_angle DOUBLE PRECISION;
    sin_angle DOUBLE PRECISION;
BEGIN
    rad_angle := NEW.Rotation * PI() / 180.0;
    cos_angle := COS(rad_angle);
    sin_angle := SIN(rad_angle);

    NEW.PAx := NEW.CenterX + (NEW.Width / 2) * cos_angle - (NEW.Height / 2) * sin_angle;
    NEW.PAy := NEW.CenterY + (NEW.Width / 2) * sin_angle + (NEW.Height / 2) * cos_angle;
    NEW.PBx := NEW.CenterX - (NEW.Width / 2) * cos_angle - (NEW.Height / 2) * sin_angle;
    NEW.PBy := NEW.CenterY - (NEW.Width / 2) * sin_angle + (NEW.Height / 2) * cos_angle;
    NEW.PCx := NEW.CenterX - (NEW.Width / 2) * cos_angle + (NEW.Height / 2) * sin_angle;
    NEW.PCy := NEW.CenterY - (NEW.Width / 2) * sin_angle - (NEW.Height / 2) * cos_angle;
    NEW.PDx := NEW.CenterX + (NEW.Width / 2) * cos_angle + (NEW.Height / 2) * sin_angle;
    NEW.PDy := NEW.CenterY + (NEW.Width / 2) * sin_angle - (NEW.Height / 2) * cos_angle;
   
    NEW.MinX := LEAST(NEW.PAx, NEW.PBx, NEW.PCx, NEW.PDx);
    NEW.MaxX := GREATEST(NEW.PAx, NEW.PBx, NEW.PCx, NEW.PDx);
    NEW.MinY := LEAST(NEW.PAy, NEW.PBy, NEW.PCy, NEW.PDy);
    NEW.MaxY := GREATEST(NEW.PAy, NEW.PBy, NEW.PCy, NEW.PDy);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_rectangle_vertices
BEFORE INSERT OR UPDATE ON Rectangles
FOR EACH ROW EXECUTE PROCEDURE calculate_vertices_and_bounds();

CREATE INDEX idx_minx ON Rectangles(MinX);
CREATE INDEX idx_maxx ON Rectangles(MaxX);
CREATE INDEX idx_miny ON Rectangles(MinY);
CREATE INDEX idx_maxy ON Rectangles(MaxY);

- FILLING SCRIPT:
DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..100000 LOOP
        INSERT INTO Rectangles (CenterX, CenterY, Width, Height, Rotation)
        VALUES (
            RANDOM() * 2000 - 1000,  -- CenterX
            RANDOM() * 2000 - 1000,  -- CenterY
            RANDOM() * 500 + 1,      -- Width
            RANDOM() * 500 + 1,      -- Height
            RANDOM() * 360           -- Rotation
        );
    END LOOP;
END $$;
