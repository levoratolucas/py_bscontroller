from app.view.frontend.screens.relatorios.cards.card_base import CardBase

class CardRepetido(CardBase):
    def __init__(self, parent, row, col, callback=None):
        super().__init__(
            parent=parent,
            row=row,
            col=col,
            texto="REPETIDO",
            icone="🔄",
            cor="#ff6b00",
            callback=callback
        )