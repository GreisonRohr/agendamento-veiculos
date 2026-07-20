from datetime import date

from app.extensions import db
from app.models import Manutencao, Veiculo


class ManutencaoService:

    @staticmethod
    def listar():
        return (
            Manutencao.query
            .order_by(Manutencao.data_inicio.desc())
            .all()
        )

    @staticmethod
    def buscar_por_id(id):
        return Manutencao.query.get_or_404(id)

    @staticmethod
    def criar(form):

        manutencao = Manutencao(
            veiculo_id=form.veiculo.data,
            tipo=form.tipo.data,
            descricao=form.descricao.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            custo=form.custo.data,
            status=form.status.data,
            oficina=form.oficina.data
        )

        db.session.add(manutencao)

        # Atualiza status do veículo para "Manutenção"
        if manutencao.status == "Em andamento":
            veiculo = Veiculo.query.get(form.veiculo.data)
            if veiculo:
                veiculo.status = "Manutenção"

        db.session.commit()

        return manutencao

    @staticmethod
    def atualizar(id, form):

        manutencao = Manutencao.query.get_or_404(id)

        manutencao.veiculo_id = form.veiculo.data
        manutencao.tipo = form.tipo.data
        manutencao.descricao = form.descricao.data
        manutencao.data_inicio = form.data_inicio.data
        manutencao.data_fim = form.data_fim.data
        manutencao.custo = form.custo.data
        manutencao.status = form.status.data
        manutencao.oficina = form.oficina.data

        # Atualiza status do veículo conforme manutenção
        veiculo = Veiculo.query.get(form.veiculo.data)
        if veiculo:
            if manutencao.status == "Em andamento":
                veiculo.status = "Manutenção"
            elif manutencao.status == "Concluída":
                veiculo.status = "Disponível"

        db.session.commit()

        return manutencao

    @staticmethod
    def excluir(id):

        manutencao = Manutencao.query.get_or_404(id)

        # Libera o veículo se a manutenção estava em andamento
        if manutencao.status == "Em andamento":
            veiculo = Veiculo.query.get(manutencao.veiculo_id)
            if veiculo:
                veiculo.status = "Disponível"

        db.session.delete(manutencao)
        db.session.commit()

    @staticmethod
    def manutencoes_ativas():
        return (
            Manutencao.query
            .filter_by(status="Em andamento")
            .order_by(Manutencao.data_inicio.desc())
            .all()
        )

    @staticmethod
    def custo_total():
        total = db.session.query(
            func.sum(Manutencao.custo)
        ).scalar()
        return total or 0
