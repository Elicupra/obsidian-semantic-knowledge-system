# Issues detectadas

## [Alta] Frontmatter duplicado en notas generadas

- **Archivo**: src/semantix/ingest.py + src/semantix/generate.py
- **Categoría**: calidad
- **Descripción**: El prompt del LLM genera un frontmatter YAML dentro del contenido de la nota, y luego generate.py añade otro frontmatter al inicio. Esto resulta en frontmatter duplicado.
- **Severidad**: Alta

### Código relevante
El prompt en ingest.py solicita:
```
### 1. Frontmatter YAML
Incluye: title, source, source_type...
```

Y generate.py añade:
```python
if self.include_metadata:
    metadata = {...}
    lines.append("---")
    lines.append(self._simple_yaml_dump(metadata))
```

### Propuesta de solución
1. Modificar el prompt para que NO genere frontmatter dentro del contenido
2. Opcionalmente, extraer el frontmatter generado por el LLM y pasarlo a generate.py
3. Alternativamente, añadir flag para decidir si usar metadata del LLM o del sistema

---

## [Media] Excepciones demasiado amplias (catch-all)

- **Archivo**: src/semantix/ingest.py:94, :101, :171
- **Categoría**: calidad
- **Descripción**: Uso de `except Exception:` sin logging ni manejo específico. Puede ocultar errores importantes.
- **Severidad**: Media

### Código relevante
```python
except Exception as e:
    return f"# Error al procesar\n\n{str(e)}..."

except Exception:
    return False
```

### Propuesta de solución
1. Logging de errores para debugging
2. Manejar excepciones específicas donde sea posible
3. Considerar exceptions personalizadas

---

## [Media] Falta de tests

- **Archivo**: Proyecto completo
- **Categoría**: testing
- **Descripción**: No existe directorio tests/ ni tests unitarios.
- **Severidad**: Media

### Propuesta de solución
1. Crear directorio tests/
2. Añadir tests para Ingestor, NoteGenerator, providers
3. Usar pytest (ya en dependencias dev)

---

## [Baja] Dependencias obsoletas

- **Archivo**: pyproject.toml
- **Categoría**: deps
- **Descripción**: Muchas dependencias tienen versiones más recientes disponibles.
- **Severidad**: Baja

### Paquetes con updates disponibles
- click: 8.3.1 -> 8.3.3
- requests: 2.32.5 -> 2.34.0
- pydantic: 2.12.5 -> 2.13.4
- python-dotenv: 1.2.1 -> 1.2.2

### Propuesta de solución
```bash
pip install -U click requests pydantic python-dotenv
```

---

## [Baja] Sin validación de inputs en ingest

- **Archivo**: src/semantix/ingest.py
- **Categoría**: calidad
- **Descripción**: No hay validación del tamaño del contenido antes de pasarlo al LLM (se limita a 15000 chars pero no se valida input vacío).
- **Severidad**: Baja

### Propuesta de solución
1. Validar que content no esté vacío antes de llamar al LLM
2. Validar longitud máxima de URL

---

## [Info] .gitignore básico

- **Archivo**: .opencode/.gitignore
- **Categoría**: git
- **Descripción**: Solo existe un .gitignore básico en .opencode, pero no en raíz del proyecto.
- **Severidad**: Info

### Propuesta de solución
Crear .gitignore en raíz con:
```
__pycache__/
*.pyc
.env
.venv/
venv/
*.egg-info/
```

---

## Resumen

| Severidad | Cantidad |
|-----------|----------|
| Alta      | 1        |
| Media     | 2        |
| Baja      | 2        |
| Info      | 1        |
| **Total** | **6**    |