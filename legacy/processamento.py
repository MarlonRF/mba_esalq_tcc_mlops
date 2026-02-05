        caminho_entrada: str, caminho_saida: str, cfg: Dict = None
    ):
        df = pd.read_csv(caminho_entrada)
        dfp, arts = step_processar_dataframe(df=df, cfg=cfg)
        _garantir_diretorio_existe(caminho_saida)
        dfp.to_csv(caminho_saida, index=False)
        print(f"Processado -> {caminho_saida}")
        # opcional: subir artefatos
        try:
            from clearml import Task

            task = Task.current_task()
            if task and arts:
                for k, v in arts.items():
                    task.upload_artifact(k, v)
        except Exception as e:
            print(f"Aviso: Não foi possível fazer upload dos artefatos para ClearML: {e}")
            # Continua sem upload do ClearML


# =========================
# CLI
# =========================


def _load_cfg(path: Optional[str]) -> Optional[Dict]:
    if not path:
        return None
    txt = open(path, "r", encoding="utf-8").read()
    if path.endswith((".yaml", ".yml")):
        import yaml

        return yaml.safe_load(txt)
    return json.loads(txt)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--config")  # yaml/json
    ap.add_argument("--run-locally", action="store_true")
    args = ap.parse_args()

    cfg = _load_cfg(args.config)

    if _CLEARML_DISPONIVEL and args.run_locally:
        PipelineDecorator.run_locally()
        pipeline_processamento_novo(args.entrada, args.saida, cfg)
    else:
        processar_arquivo(args.entrada, args.saida, cfg)
