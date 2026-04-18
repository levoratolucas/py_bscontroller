from app.view.frontend.screens.relatorios.cards.card_base import CardBase

class CardImprocedente(CardBase):
    def __init__(self, parent, row, col, callback=None):
        super().__init__(
            parent=parent,
            row=row,
            col=col,
            texto="IMPROCEDENTE",
            icone="❌",
            cor="#ff3333",
            callback=callback
        )