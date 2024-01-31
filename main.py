from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

# Model

class Movie(BaseModel):
    id: Optional[int] = None
    #title: str = Field(default="Mi Película", min_length=1, max_length=100)
    #overview: str = Field(default="Mi descripción", min_length=1, max_length=100)
    title: str = Field( min_length=1, max_length=100)
    overview: str = Field( min_length=1, max_length=100)
    year: int = Field( ge=1900, le=2022)
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Mi Película",
                "overview": "Mi descripción",
                "year": 2022,
                "rating": 9.5,
                "category": "Drama"
            }
        }

# App

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

movies = [
    {
		"id": 1,
		"title": "En busca de la Felicidad",
		"overview": "La vida es una lucha para Chris Gardner. Expulsado de su apartamento, él y su joven hijo se encuentran solos sin ningún lugar a donde ir. A pesar de que Chris ocasionalmente consigue trabajo como interno en una prestigiada firma financiera, la posición no le da dinero. El dúo debe vivir en un albergue y enfrentar muchas dificultades, pero Chris no se da por vencido y lucha por conseguir una vida mejor para él y su hijo. Al final logra convertirse en un hombre multimillonario",
		"year": "2006",
		"rating": 9.2,
		"category": "Drama"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'] , response_model=Movie )
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

# Parámetro Query Se le agregar una barra al final, para diferenciarlo de get_movies
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=1, max_length=100)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    return JSONResponse(content=data)

# Parámetro Body)

@app.post('/movies', tags=['movies'] , response_model=dict)
def create_movie(movie : Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message":"Se ha creado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(content={"message":"Se ha modificado la película"})

@app.delete('/movies/{id}', tags=['movies'] , response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se ha eliminado"})