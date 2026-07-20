from app.extensions import db
from app.models import Veiculo


class VeiculoService:

    @staticmethod
    def listar():
        return (
            Veiculo.query
            .filter_by(ativo=True)
            .order_by(Veiculo.placa)
            .all()
        )

    @staticmethod
    def listar_disponiveis_para_agendamento():
        """Retorna apenas veículos que podem ser agendados."""
        return (
            Veiculo.query
            .filter_by(
                ativo=True,
                status="Disponível"
            )
            .order_by(Veiculo.placa)
            .all()
        )

    @staticmethod
    def buscar_por_id(id):
        return Veiculo.query.get_or_404(id)

    @staticmethod
    def buscar_por_placa(placa):
        return Veiculo.query.filter_by(
            placa=placa.upper()
        ).first()

    @staticmethod
    def criar(form):

        veiculo = Veiculo(
            placa=form.placa.data.upper(),
            marca=form.marca.data,
            modelo=form.modelo.data,
            ano=form.ano.data,
            cor=form.cor.data,
            unidade=form.unidade.data,
            km_atual=form.km_atual.data,
            status=form.status.data,
            ultima_revisao=form.ultima_revisao.data,
            proxima_revisao=form.proxima_revisao.data,
            observacoes=form.observacoes.data,
        )

        db.session.add(veiculo)
        db.session.commit()

        return veiculo

    @staticmethod
    def atualizar(id, form):

        veiculo = Veiculo.query.get_or_404(id)

        veiculo.placa = form.placa.data.upper()
        veiculo.marca = form.marca.data
        veiculo.modelo = form.modelo.data
        veiculo.ano = form.ano.data
        veiculo.cor = form.cor.data
        veiculo.unidade = form.unidade.data
        veiculo.km_atual = form.km_atual.data
        veiculo.status = form.status.data
        veiculo.ultima_revisao = form.ultima_revisao.data
        veiculo.proxima_revisao = form.proxima_revisao.data
        veiculo.observacoes = form.observacoes.data

        db.session.commit()

        return veiculo

    @staticmethod
    def excluir(id):

        veiculo = Veiculo.query.get_or_404(id)

        veiculo.ativo = False

        db.session.commit()

    @staticmethod
    def buscar_por_placa_inativa(placa):

        return (
            Veiculo.query
            .filter_by(
                placa=placa.upper(),
                ativo=False
            )
            .first()
        )

    @staticmethod
    def reativar(id, form):

        veiculo = Veiculo.query.get_or_404(id)

        veiculo.ativo = True

        veiculo.placa = form.placa.data.upper()
        veiculo.marca = form.marca.data
        veiculo.modelo = form.modelo.data
        veiculo.ano = form.ano.data
        veiculo.cor = form.cor.data
        veiculo.unidade = form.unidade.data
        veiculo.km_atual = form.km_atual.data
        veiculo.status = form.status.data
        veiculo.ultima_revisao = form.ultima_revisao.data
        veiculo.proxima_revisao = form.proxima_revisao.data
        veiculo.observacoes = form.observacoes.data

        db.session.commit()

        return veiculo
