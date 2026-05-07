import click
from pathlib import Path
from semantix.ingest import Ingestor
from semantix.generate import NoteGenerator
from semantix.models import ModelProvider


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Semantix - CLI para ingestión de conocimiento en Obsidian"""
    pass


@main.command()
@click.option("--input", "-i", required=True, help="Archivo, URL o path a procesar")
@click.option("--vault", "-v", required=True, type=click.Path(exists=True), help="Ruta al vault de Obsidian")
@click.option("--model", "-m", default="auto", type=click.Choice(["gemini", "claude", "local", "auto"]), help="Modelo a usar")
@click.option("--category", "-c", default=None, help="Categoría/carpeta destino")
@click.option("--metadata/--no-metadata", default=True, help="Incluir metadata YAML")
@click.option("--verbose", "-vv", is_count=True, help="Modo verbose")
def ingest(input, vault, model, category, metadata, verbose):
    """Procesa un archivo/URL y genera nota en Obsidian"""
    ingestor = Ingestor(ModelProvider(model))
    result = ingestor.process(input)
    
    generator = NoteGenerator(Path(vault), include_metadata=metadata)
    output_path = generator.generate(result, category=category)
    
    click.echo(f"Nota creada: {output_path}")
    if verbose:
        click.echo(f"Etiquetas: {result.get('tags', [])}")


@main.command()
@click.option("--vault", "-v", required=True, type=click.Path(exists=True), help="Ruta al vault de Obsidian")
def deduplicate(vault):
    """Detecta y reporta notas duplicadas en el vault."""
    from semantix.dedupe import Deduplicator
    dedup = Deduplicator(Path(vault))
    duplicates = dedup.find_duplicates()
    
    if not duplicates:
        click.echo("No se encontraron duplicados.")
    else:
        click.echo(f"Se encontraron {len(duplicates)} grupos de duplicados.")
        for group in duplicates:
            click.echo(f"  - {group}")


@main.command()
@click.option("--vault", "-v", required=True, type=click.Path(exists=True), help="Ruta al vault de Obsidian")
def backlinks(vault):
    """Genera reporte de backlinks en el vault."""
    from semantix.backlinks import BacklinkManager
    bm = BacklinkManager(Path(vault))
    report = bm.generate_report()
    
    click.echo(f"Total de notas: {report['total_notes']}")
    click.echo(f"Total de backlinks: {report['total_backlinks']}")


if __name__ == "__main__":
    main()
