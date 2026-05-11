import click
from pathlib import Path
from semantix.ingest import Ingestor
from semantix.generate import NoteGenerator
from semantix.models import ModelProvider, get_provider, list_providers
from semantix.config import (
    init as config_init,
    set_api_key,
    remove_api_key,
    get_default_provider,
    set_default_provider,
    show_config,
    get_configured_providers,
    PROVIDER_INFO,
    AVAILABLE_PROVIDERS,
)


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Semantix - CLI para ingestion de conocimiento en Obsidian"""
    config_init()


@main.command()
@click.option("--input", "-i", required=True, help="Archivo, URL o path a procesar")
@click.option("--vault", "-v", required=True, type=click.Path(exists=True), help="Ruta al vault de Obsidian")
@click.option("--model", "-m", default="auto", type=click.Choice(list_providers()), help="Modelo a usar")
@click.option("--summarize/--no-summarize", default=True, help="Usar LLM para resumir contenido")
@click.option("--category", "-c", default=None, help="Categoria/carpeta destino")
@click.option("--metadata/--no-metadata", default=True, help="Incluir metadata YAML")
@click.option("--verbose", "-vv", count=True, help="Modo verbose")
def ingest(input, vault, model, category, metadata, verbose, summarize):
    """Procesa un archivo/URL y genera nota en Obsidian"""
    provider = get_provider(model)
    ingestor = Ingestor(provider)
    result = ingestor.process(input)
    
    content = result.get("content", result.get("description", ""))
    title = result.get("title", "Sin titulo")
    
    if summarize and content:
        click.echo("Generando resumen con LLM...")
        result["content"] = ingestor.summarize(content, title)
    
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


@click.group(name="config")
def config_group():
    """Gestiona la configuración de API keys"""
    pass


@config_group.command(name="show")
def config_show():
    """Muestra configuración actual"""
    show_config()


@config_group.command(name="set")
@click.option("--key", "-k", help="API key directamente")
@click.option("--provider", "-p", type=click.Choice(AVAILABLE_PROVIDERS), help="Proveedor a configurar")
def config_set(key, provider):
    """Configura API key para un proveedor"""
    if not provider:
        click.echo("Selecciona un proveedor:\n")
        for i, p in enumerate(AVAILABLE_PROVIDERS, 1):
            info = PROVIDER_INFO[p]
            click.echo(f"  {i}. {p} - {info['name']}: {info['description']}")
        
        choice = click.prompt("\nNúmero del proveedor", type=int)
        if choice < 1 or choice > len(AVAILABLE_PROVIDERS):
            click.echo("Selección inválida")
            return
        provider = AVAILABLE_PROVIDERS[choice - 1]
    
    if provider == "local":
        click.echo("El provider 'local' no requiere API key")
        return
    
    if not key:
        key = click.prompt(f"Introduce API key para {provider}", hide_input=True)
    
    set_api_key(provider, key)
    click.echo(f"[OK] API key guardada para {provider}")


@config_group.command(name="remove")
@click.option("--provider", "-p", type=click.Choice(AVAILABLE_PROVIDERS), help="Proveedor a eliminar")
def config_remove(provider):
    """Elimina API key guardada"""
    if not provider:
        configured = get_configured_providers()
        if not configured:
            click.echo("No hay proveedores configurados")
            return
        
        click.echo("Selecciona proveedor a eliminar:\n")
        for i, p in enumerate(configured, 1):
            click.echo(f"  {i}. {p}")
        
        choice = click.prompt("\nNúmero del proveedor", type=int)
        if choice < 1 or choice > len(configured):
            click.echo("Selección inválida")
            return
        provider = configured[choice - 1]
    
    remove_api_key(provider)
    click.echo(f"[OK] API key eliminada para {provider}")


@config_group.command(name="default")
@click.option("--provider", "-p", type=click.Choice(AVAILABLE_PROVIDERS), required=True, help="Proveedor por defecto")
def config_default(provider):
    """Establece proveedor por defecto"""
    set_default_provider(provider)
    click.echo(f"[OK] Proveedor por defecto: {provider}")


main.add_command(config_group)


if __name__ == "__main__":
    main()
