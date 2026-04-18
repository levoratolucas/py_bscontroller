from app.view.frontend.screens.relatorios.cards.card_base import CardBase

class CardPendente(CardBase):
    def __init__(self, parent, row, col, callback=None):
        super().__init__(
            parent=parent,
            row=row,
            col=col,
            texto="PENDENTE",
            icone="⏳",
            cor="#ff8800",
            callback=callback
        )