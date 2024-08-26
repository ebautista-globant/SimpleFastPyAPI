from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

app = FastAPI()

# SQLAlchemy model
Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    species = Column(String)
    homeworld = Column(String)
    appearances = Column(String)
    affiliations = Column(String)
    locations = Column(String)
    dimensions = Column(String)
    weapons = Column(String)
    vehicles = Column(String)
    tools = Column(String)

# SQLAlchemy database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./star_wars.db"  # SQLite database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic model
class Character(BaseModel):
    name: str
    description: str
    appearances: List[str] = []
    affiliations: List[str] = []
    locations: List[str] = []
    dimensions: List[str] = []
    weapons: List[str] = []
    vehicles: List[str] = []
    tools: List[str] = []

# Scrape character endpoint
@app.post("/scrape_character")
async def scrape_character(url: str, db: Session = Depends(get_db)):
    # Fetch the HTML content from the website
    response = requests.get(url)
    html = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the character information from the HTML
    name = soup.find('span', class_='long-title').text.strip()
    description = soup.find('p', class_='desc').text.strip()
    appearances = [a.text.strip() for a in soup.select('.category:has(.heading:contains("Appearances")) a')]
    affiliations = [a.text.strip() for a in soup.select('.category:has(.heading:contains("Affiliations")) a')]
    locations = [a.text.strip() for a in soup.select('.category:has(.heading:contains("Locations")) a')]
    dimensions = [d.text.strip() for d in soup.select('.category:has(.heading:contains("Dimensions")) .property-name')]
    weapons = [w.text.strip() for w in soup.select('.category:has(.heading:contains("Weapons")) a')]
    vehicles = [v.text.strip() for v in soup.select('.category:has(.heading:contains("Vehicles")) a')]
    tools = [t.text.strip() for t in soup.select('.category:has(.heading:contains("Tool")) a')]

    # Insert the character data into the database using SQLAlchemy
    character_data = Character(
        name=name,
        description=description,
        appearances=",".join(appearances),
        affiliations=",".join(affiliations),
        locations=",".join(locations),
        dimensions=",".join(dimensions),
        weapons=",".join(weapons),
        vehicles=",".join(vehicles),
        tools=",".join(tools)
    )
    db.add(character_data)
    db.commit()
    db.refresh(character_data)

    # Return the scraped character data
    character = Character(
        name=name,
        description=description,
        appearances=appearances,
        affiliations=affiliations,
        locations=locations,
        dimensions=dimensions,
        weapons=weapons,
        vehicles=vehicles,
        tools=tools
    )
    return character

@app.post("/manualy_create_character")
async def create_character(
    name: str,
    description: str,
    appearances: List[str] = [],
    affiliations: List[str] = [],
    locations: List[str] = [],
    dimensions: List[str] = [],
    weapons: List[str] = [],
    vehicles: List[str] = [],
    tools: List[str] = [],
    db: Session = Depends(get_db)
):
    character_data = Character(
        name=name,
        description=description,
        appearances=",".join(appearances),
        affiliations=",".join(affiliations),
        locations=",".join(locations),
        dimensions=",".join(dimensions),
        weapons=",".join(weapons),
        vehicles=",".join(vehicles),
        tools=",".join(tools)
    )
    db.add(character_data)
    db.commit()
    db.refresh(character_data)
    return character_data