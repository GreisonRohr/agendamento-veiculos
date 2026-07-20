from sqlalchemy import func

from app.extensions import db
from app.models import Veiculo, Agendamento, Manutencao


class RelatorioService:

    @staticmethod
    def utilizacao_frota():
        """Relatório de utilização da frota."""

        veiculos = Veiculo.query.filter_by(ativo=True).all()

        dados = []

        for veiculo in veiculos:

            total_agendamentos = Agendamento.query.filter_by(
                veiculo_id=veiculo.id
            ).count()

            total_manutencoes = Manutencao.query.filter_by(
                veiculo_id=veiculo.id
            ).count()

            custo_manutencoes = db.session.query(
                func.sum(Manutencao.custo)
            ).filter_by(
                veiculo_id=veiculo.id
            ).scalar() or 0

            dados.append({
                "veiculo": veiculo,
                "total_agendamentos": total_agendamentos,
                "total_manutencoes": total_manutencoes,
                "custo_manutencoes": custo_manutencoes,
            })

        # Ordena por mais utilizado
        dados.sort(key=lambda x: x["total_agendamentos"], reverse=True)

        return dados

    @staticmethod
    def resumo_geral():
        """Resumo geral do sistema."""

        return {
            "total_veiculos": Veiculo.query.filter_by(ativo=True).count(),
            "total_agendamentos": Agendamento.query.count(),
            "total_manutencoes": Manutencao.query.count(),
            "agendamentos_ativos": Agendamento.query.filter(
                Agendamento.status != "Cancelado"
            ).count(),
            "manutencoes_ativas": Manutencao.query.filter_by(
                status="Em andamento"
            ).count(),
            "custo_total_manutencoes": db.session.query(
                func.sum(Manutencao.custo)
            ).scalar() or 0,
            "veiculos_disponiveis": Veiculo.query.filter_by(
                ativo=True, status="Disponível"
            ).count(),
            "veiculos_manutencao": Veiculo.query.filter_by(
                ativo=True, status="Manutenção"
            ).count(),
        }

    @staticmethod
    def agendamentos_por_periodo(data_inicio, data_fim):
        """Agendamentos em um período específico."""

        return (
            Agendamento.query
            .filter(
                Agendamento.data_saida >= data_inicio,
                Agendamento.data_saida <= data_fim
            )
            .order_by(Agendamento.data_saida)
            .all()
        )

    @staticmethod
    def manutencoes_por_periodo(data_inicio, data_fim):
        """Manutenções em um período específico."""

        return (
            Manutencao.query
            .filter(
                Manutencao.data_inicio >= data_inicio,
                Manutencao.data_inicio <= data_fim
            )
            .order_by(Manutencao.data_inicio)
            .all()
        )
