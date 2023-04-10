from enum import Enum
from dataclasses import dataclass
from random import randint

# Enumeracion de los tipos de fuentes de informacion y su pesos
class SourceType(Enum):
    
    Essential = 0.6 # Peso de la fuente
    Cardinal = 0.5 


@dataclass
class Row:
    """
    Fila de la tabla que contiene el valor de la informacion y el tipo de fuente
    """

    # Valor de la informacion
    value: float

    # Tipo de fuente
    source_type: SourceType

    # nombre de la fuente (opcional)
    source_name: str = None 


class Table:
    """
    Tabla de los registro o informacion que se han evaluados
    """

    def __init__(self, rows: list[Row]) -> None:
        # Lista de tuplas que contienen el valor de la informacion y el tipo de fuente, cada tupla es una fila
        self.rows: list[Row] = rows

    def resolve(self) -> int:
        """
        Hace los calculos para procesar la informacion y obtener el nivel del usuario
        """
        
        """
        Calcula el puntaje de las fuentes esenciales

        Formula: FE = Suma de los valores de las fuentes esenciales, cada valor se multiplica por el peso de la fuente
        """
        FE = sum(
            map(
                lambda row: row.value * row.source_type.value,
                filter(lambda row: row.source_type == SourceType.Essential, self.rows),
            )
        )

        """
        Calcula el puntaje de las fuentes cardinales
        
        Formula: Misma que la anterior
        """
        FC = sum(
            map(
                lambda row: row.value * row.source_type.value,
                filter(lambda row: row.source_type == SourceType.Cardinal, self.rows),
            )
        )


        """
        Calcula el puntaje de las fuentes

        Formula: PG = peso de la fuente (Essential) * FE + peso de la fuente (Cardinal) * FC
        """

        PG = SourceType.Essential.value * FE + SourceType.Cardinal.value * FC

        """
        Calcula el nivel del usuario
    
        Formula: 1 divide entre el numero de fuentes categorizadas, multiplicadopor el sumatorio de n, i=1, multiplicado por peso de la fuente i * puntaje de la fuente i 
        """

        Nivel = int(1 / len(self.rows) * sum(
            map(
                lambda row: row.source_type.value * row.value,
                self.rows,
            )
        ))

        return Nivel



# TEST ----------------------------

def roll_table():
    """
    Crea una tabla con los valores aleatorios
    """

    # Crea la tabla
    table = Table([
        Row(randint(25, 50), SourceType.Essential, "Certificaciones"),
        Row(randint(5, 25), SourceType.Essential, "Educacion"),
        Row(randint(5, 30), SourceType.Essential, "Evaluaciones"),
        Row(randint(10, 50), SourceType.Essential, "Experiencia"),
        Row(randint(5, 20), SourceType.Cardinal, "Actividad"),
        Row(randint(5, 30), SourceType.Cardinal, "Proyectos"),
        Row(randint(5, 25), SourceType.Cardinal, "Contribuciones"),
        Row(randint(5, 20), SourceType.Cardinal, "Voluntariedad")
    ])

    res = table.resolve()

    return res


if __name__ == "__main__":
    levels = []
    for _ in range(100):
        levels.append(roll_table())


    # Stats de los niveles
    print()
    print("Stats de los niveles")
    print(f"Min: {min(levels)}")
    print(f"Max: {max(levels)}")
    print(f"Promedio: {sum(levels) / len(levels)}")
