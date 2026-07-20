from datetime import date, datetime

from sqlalchemy import func

from app.extensions import db
from app.models import Veiculo, Agendamento, Manutencao


class DashboardService:

    @staticmethod
    def indicadores():

        total_custo_manutencao = db.session.query(
            func.sum(Manutencao.custo)
        ).filter(Manutencao.status == "Em andamento").scalar() or 0

        return {
            "total_veiculos": Veiculo.query.filter_by(
                ativo=True
            ).count(),

            "disponiveis": Veiculo.query.filter_by(
                ativo=True,
                status="Disponível"
            ).count(),

            "manutencao": Veiculo.query.filter_by(
                ativo=True,
                status="Manutenção"
            ).count(),

            "agendamentos_hoje": Agendamento.query.filter_by(
                data_saida=date.today()
            ).count(),

            "custo_manutencao": total_custo_manutencao,
        }

    @staticmethod
    def proximos_agendamentos():

        agendamentos = (
            Agendamento.query
            .filter(
                Agendamento.data_saida >= date.today()
            )
            .order_by(
                Agendamento.data_saida,
                Agendamento.hora_saida
            )
            .limit(10)
            .all()
        )

        # Atualiza status automaticamente
        agora = datetime.now()
        for a in agendamentos:
            if a.status in ["Agendado", "Em andamento"]:
                inicio = datetime.combine(a.data_saida, a.hora_saida)
                fim = datetime.combine(a.data_retorno, a.hora_retorno)

                if inicio <= agora <= fim:
                    a.status = "Em andamento"
                elif agora > fim:
                    a.status = "Finalizado"

        db.session.commit()

        return agendamentos

    @staticmethod
    def retornos_hoje():

        return (
            Agendamento.query
            .filter(
                Agendamento.data_retorno == date.today()
            )
            .order_by(
                Agendamento.hora_retorno
            )
            .all()
        )

    @staticmethod
    def proximas_revisoes():

        return (
            Veiculo.query
            .filter(
                Veiculo.proxima_revisao != None,
                Veiculo.ativo == True
            )
            .order_by(
                Veiculo.proxima_revisao
            )
            .limit(10)
            .all()
        )

    @staticmethod
    def manutencoes_ativas():
        """Retorna manutenções reais em andamento com detalhes."""
        return (
            Manutencao.query
            .filter_by(status="Em andamento")
            .order_by(Manutencao.data_inicio.desc())
            .limit(10)
            .all()
        )

    @staticmethod
    def manutencoes():

        return (
            Veiculo.query
            .filter_by(
                ativo=True,
                status="Manutenção"
            )
            .all()
        )
