from typing import List, Set, Union, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from penny_ante.space import Space
    from penny_ante.layout import Layout
    from penny_ante.chips import Chips
    from penny_ante.betting_rules import BettingRules


class BetType(Enum):
    """Enumeration of all possible roulette bet types."""

    # Inside bets
    STRAIGHT_UP = "straight_up"  # Single number
    SPLIT = "split"  # Two adjacent numbers
    STREET = "street"  # Three numbers in a row
    CORNER = "corner"  # Four numbers in a square
    SIX_LINE = "six_line"  # Six numbers in two adjacent rows

    # Outside bets
    RED = "red"  # All red numbers
    BLACK = "black"  # All black numbers
    ODD = "odd"  # All odd numbers
    EVEN = "even"  # All even numbers
    HIGH = "high"  # Numbers 19-36
    LOW = "low"  # Numbers 1-18
    FIRST_DOZEN = "first_dozen"  # Numbers 1-12
    SECOND_DOZEN = "second_dozen"  # Numbers 13-24
    THIRD_DOZEN = "third_dozen"  # Numbers 25-36
    FIRST_COLUMN = "first_column"  # First column (1,4,7,10,13,16,19,22,25,28,31,34)
    SECOND_COLUMN = "second_column"  # Second column (2,5,8,11,14,17,20,23,26,29,32,35)
    THIRD_COLUMN = "third_column"  # Third column (3,6,9,12,15,18,21,24,27,30,33,36)


class Bet:
    """
    Represents a bet placed on a roulette table.

    A bet encompasses the type of bet, the spaces it covers, the amount wagered,
    and provides methods for validation and payout calculation.

    Attributes:
        bet_type (BetType): The type of bet being placed
        spaces (Set[str]): The space values covered by this bet
        amount (int): The amount wagered (in chip count)
        chips (Optional[Chips]): The chips used for this bet
        layout_positions (List[tuple]): Layout positions covered by this bet
    """

    # Payout ratios for each bet type (amount won per unit bet, not including original bet)
    PAYOUT_RATIOS = {
        BetType.STRAIGHT_UP: 35,
        BetType.SPLIT: 17,
        BetType.STREET: 11,
        BetType.CORNER: 8,
        BetType.SIX_LINE: 5,
        BetType.RED: 1,
        BetType.BLACK: 1,
        BetType.ODD: 1,
        BetType.EVEN: 1,
        BetType.HIGH: 1,
        BetType.LOW: 1,
        BetType.FIRST_DOZEN: 2,
        BetType.SECOND_DOZEN: 2,
        BetType.THIRD_DOZEN: 2,
        BetType.FIRST_COLUMN: 2,
        BetType.SECOND_COLUMN: 2,
        BetType.THIRD_COLUMN: 2,
    }

    def __init__(
        self,
        bet_type: BetType,
        spaces: Union[List[str], Set[str], str],
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> None:
        """
        Initialize a new bet.

        Args:
            bet_type: The type of bet being placed
            spaces: The space value(s) covered by this bet
            amount: The amount being wagered (in chip count)
            chips: The chips being used for this bet
            layout: The layout to validate against
            betting_rules: The betting rules configuration to use

        Raises:
            ValueError: If the bet configuration is invalid
        """
        self.bet_type = bet_type
        self.amount = amount
        self.chips = chips
        self.betting_rules = betting_rules

        # Normalize spaces to a set of strings
        if isinstance(spaces, str):
            self.spaces = {spaces}
        elif isinstance(spaces, list):
            self.spaces = set(spaces)
        else:
            self.spaces = spaces.copy()

        # Validate the bet
        if layout:
            self._validate_bet(layout)

        # Validate betting rules if provided
        if betting_rules:
            self._validate_betting_rules()

        # Calculate layout positions if layout is provided
        self.layout_positions: List[tuple] = []
        if layout:
            self.layout_positions = self._calculate_layout_positions(layout)

    def _validate_bet(self, layout: "Layout") -> None:
        """
        Validate that the bet is properly configured.

        Args:
            layout: The layout to validate against

        Raises:
            ValueError: If the bet configuration is invalid
        """
        if self.amount <= 0:
            raise ValueError("Bet amount must be positive")

        # Validate spaces exist on the layout
        for space_value in self.spaces:
            if space_value not in layout.lookup and space_value not in ["0", "00"]:
                raise ValueError(f"Invalid space value: {space_value}")

        # Validate bet type matches the spaces
        self._validate_bet_type_matches_spaces(layout)

    def _validate_betting_rules(self) -> None:
        """
        Validate bet against betting rules if provided.

        Raises:
            ValueError: If bet violates betting rules
        """
        if not self.betting_rules:
            return

        # Check if bet type is allowed
        if not self.betting_rules.is_bet_allowed(self.bet_type):
            raise ValueError(
                f"Bet type {self.bet_type.value} is not allowed on this table"
            )

        # Check bet amount limits
        if not self.betting_rules.validate_bet_amount(self.bet_type, self.amount):
            min_bet = self.betting_rules.get_minimum_bet(self.bet_type)
            max_bet = self.betting_rules.get_maximum_bet(self.bet_type)
            raise ValueError(
                f"Bet amount {self.amount} is outside allowed range [{min_bet}, {max_bet}] for {self.bet_type.value}"
            )

    def _validate_bet_type_matches_spaces(self, layout: "Layout") -> None:
        """
        Validate that the bet type matches the provided spaces.

        Args:
            layout: The layout to validate against

        Raises:
            ValueError: If the bet type doesn't match the spaces
        """
        if self.bet_type == BetType.STRAIGHT_UP:
            if len(self.spaces) != 1:
                raise ValueError("Straight up bet must cover exactly one space")

        elif self.bet_type == BetType.SPLIT:
            if len(self.spaces) != 2:
                raise ValueError("Split bet must cover exactly two spaces")
            # Additional validation could check if spaces are adjacent

        elif self.bet_type == BetType.STREET:
            if len(self.spaces) != 3:
                raise ValueError("Street bet must cover exactly three spaces")
            # Additional validation could check if spaces form a row

        elif self.bet_type == BetType.CORNER:
            if len(self.spaces) != 4:
                raise ValueError("Corner bet must cover exactly four spaces")
            # Additional validation could check if spaces form a square

        elif self.bet_type == BetType.SIX_LINE:
            if len(self.spaces) != 6:
                raise ValueError("Six line bet must cover exactly six spaces")
            # Additional validation could check if spaces form two adjacent rows

    def _calculate_layout_positions(self, layout: "Layout") -> List[tuple]:
        """
        Calculate the layout positions covered by this bet.

        Args:
            layout: The layout to calculate positions for

        Returns:
            List of (row, column) tuples representing layout positions
        """
        positions = []
        for space_value in self.spaces:
            if space_value in layout.lookup:
                row, col = layout.lookup[space_value]
                positions.append((row, col))
        return positions

    def is_winning_bet(self, winning_space: "Space") -> bool:
        """
        Check if this bet wins against the given winning space.

        Args:
            winning_space: The space where the ball landed

        Returns:
            True if this bet wins, False otherwise
        """
        winning_value = winning_space.value

        # Check if the winning space is directly covered
        if winning_value in self.spaces:
            return True

        # Check outside bets
        if self.bet_type == BetType.RED:
            return winning_space.color == "RED"
        elif self.bet_type == BetType.BLACK:
            return winning_space.color == "BLACK"
        elif self.bet_type == BetType.ODD:
            return (
                winning_value.isdigit()
                and int(winning_value) > 0
                and int(winning_value) % 2 == 1
            )
        elif self.bet_type == BetType.EVEN:
            return (
                winning_value.isdigit()
                and int(winning_value) > 0
                and int(winning_value) % 2 == 0
            )
        elif self.bet_type == BetType.HIGH:
            return winning_value.isdigit() and 19 <= int(winning_value) <= 36
        elif self.bet_type == BetType.LOW:
            return winning_value.isdigit() and 1 <= int(winning_value) <= 18
        elif self.bet_type == BetType.FIRST_DOZEN:
            return winning_value.isdigit() and 1 <= int(winning_value) <= 12
        elif self.bet_type == BetType.SECOND_DOZEN:
            return winning_value.isdigit() and 13 <= int(winning_value) <= 24
        elif self.bet_type == BetType.THIRD_DOZEN:
            return winning_value.isdigit() and 25 <= int(winning_value) <= 36
        elif self.bet_type == BetType.FIRST_COLUMN:
            return winning_value.isdigit() and int(winning_value) in [
                1,
                4,
                7,
                10,
                13,
                16,
                19,
                22,
                25,
                28,
                31,
                34,
            ]
        elif self.bet_type == BetType.SECOND_COLUMN:
            return winning_value.isdigit() and int(winning_value) in [
                2,
                5,
                8,
                11,
                14,
                17,
                20,
                23,
                26,
                29,
                32,
                35,
            ]
        elif self.bet_type == BetType.THIRD_COLUMN:
            return winning_value.isdigit() and int(winning_value) in [
                3,
                6,
                9,
                12,
                15,
                18,
                21,
                24,
                27,
                30,
                33,
                36,
            ]

        return False

    def calculate_payout(self, winning_space: "Space") -> int:
        """
        Calculate the payout for this bet if it wins.

        Args:
            winning_space: The space where the ball landed

        Returns:
            The total payout amount (original bet + winnings), or 0 if bet loses
        """
        if not self.is_winning_bet(winning_space):
            return 0

        # Use betting rules payout ratio if available, otherwise use default
        if self.betting_rules:
            try:
                payout_ratio = self.betting_rules.get_payout_ratio(self.bet_type)
            except ValueError:
                # Fall back to default if bet type not in rules
                payout_ratio = self.PAYOUT_RATIOS[self.bet_type]
        else:
            payout_ratio = self.PAYOUT_RATIOS[self.bet_type]

        winnings = self.amount * payout_ratio
        total_payout = self.amount + winnings  # Return original bet plus winnings

        return total_payout

    def get_effective_payout_ratio(self) -> int:
        """
        Get the effective payout ratio for this bet.

        Returns:
            The payout ratio (considering betting rules if available)
        """
        if self.betting_rules and self.betting_rules.is_bet_allowed(self.bet_type):
            try:
                return self.betting_rules.get_payout_ratio(self.bet_type)
            except ValueError:
                pass
        return self.PAYOUT_RATIOS[self.bet_type]

    def get_house_edge(self) -> float:
        """
        Get the house edge for this bet type.

        Returns:
            House edge as a percentage
        """
        if self.betting_rules:
            return self.betting_rules.get_house_edge(self.bet_type)
        else:
            # Default house edge (American roulette)
            return 5.26

    @classmethod
    def create_straight_up_bet(
        cls,
        space_value: str,
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> "Bet":
        """
        Create a straight up bet on a single number.

        Args:
            space_value: The space value to bet on
            amount: The amount to wager
            chips: The chips being used
            layout: The layout to validate against
            betting_rules: The betting rules to use

        Returns:
            A new Bet object for a straight up bet
        """
        return cls(
            BetType.STRAIGHT_UP, space_value, amount, chips, layout, betting_rules
        )

    @classmethod
    def create_split_bet(
        cls,
        space1: str,
        space2: str,
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> "Bet":
        """
        Create a split bet on two adjacent numbers.

        Args:
            space1: First space value
            space2: Second space value
            amount: The amount to wager
            chips: The chips being used
            layout: The layout to validate against

        Returns:
            A new Bet object for a split bet
        """
        return cls(
            BetType.SPLIT, [space1, space2], amount, chips, layout, betting_rules
        )

    @classmethod
    def create_color_bet(
        cls,
        color: str,
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> "Bet":
        """
        Create a color bet (red or black).

        Args:
            color: 'red' or 'black'
            amount: The amount to wager
            chips: The chips being used
            layout: The layout to validate against

        Returns:
            A new Bet object for a color bet

        Raises:
            ValueError: If color is not 'red' or 'black'
        """
        color_lower = color.lower()
        if color_lower == "red":
            bet_type = BetType.RED
            # Red numbers in roulette
            spaces = [
                "1",
                "3",
                "5",
                "7",
                "9",
                "12",
                "14",
                "16",
                "18",
                "19",
                "21",
                "23",
                "25",
                "27",
                "30",
                "32",
                "34",
                "36",
            ]
        elif color_lower == "black":
            bet_type = BetType.BLACK
            # Black numbers in roulette
            spaces = [
                "2",
                "4",
                "6",
                "8",
                "10",
                "11",
                "13",
                "15",
                "17",
                "20",
                "22",
                "24",
                "26",
                "28",
                "29",
                "31",
                "33",
                "35",
            ]
        else:
            raise ValueError("Color must be 'red' or 'black'")

        return cls(bet_type, spaces, amount, chips, layout, betting_rules)

    @classmethod
    def create_dozen_bet(
        cls,
        dozen: int,
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> "Bet":
        """
        Create a dozen bet (1-12, 13-24, or 25-36).

        Args:
            dozen: 1, 2, or 3 for first, second, or third dozen
            amount: The amount to wager
            chips: The chips being used
            layout: The layout to validate against

        Returns:
            A new Bet object for a dozen bet

        Raises:
            ValueError: If dozen is not 1, 2, or 3
        """
        if dozen == 1:
            bet_type = BetType.FIRST_DOZEN
            spaces = [str(i) for i in range(1, 13)]
        elif dozen == 2:
            bet_type = BetType.SECOND_DOZEN
            spaces = [str(i) for i in range(13, 25)]
        elif dozen == 3:
            bet_type = BetType.THIRD_DOZEN
            spaces = [str(i) for i in range(25, 37)]
        else:
            raise ValueError("Dozen must be 1, 2, or 3")

        return cls(bet_type, spaces, amount, chips, layout, betting_rules)

    @classmethod
    def create_column_bet(
        cls,
        column: int,
        amount: int,
        chips: Optional["Chips"] = None,
        layout: Optional["Layout"] = None,
        betting_rules: Optional["BettingRules"] = None,
    ) -> "Bet":
        """
        Create a column bet.

        Args:
            column: 1, 2, or 3 for first, second, or third column
            amount: The amount to wager
            chips: The chips being used
            layout: The layout to validate against

        Returns:
            A new Bet object for a column bet

        Raises:
            ValueError: If column is not 1, 2, or 3
        """
        if column == 1:
            bet_type = BetType.FIRST_COLUMN
            spaces = [
                "1",
                "4",
                "7",
                "10",
                "13",
                "16",
                "19",
                "22",
                "25",
                "28",
                "31",
                "34",
            ]
        elif column == 2:
            bet_type = BetType.SECOND_COLUMN
            spaces = [
                "2",
                "5",
                "8",
                "11",
                "14",
                "17",
                "20",
                "23",
                "26",
                "29",
                "32",
                "35",
            ]
        elif column == 3:
            bet_type = BetType.THIRD_COLUMN
            spaces = [
                "3",
                "6",
                "9",
                "12",
                "15",
                "18",
                "21",
                "24",
                "27",
                "30",
                "33",
                "36",
            ]
        else:
            raise ValueError("Column must be 1, 2, or 3")

        return cls(bet_type, spaces, amount, chips, layout, betting_rules)

    def __str__(self) -> str:
        """Return a string representation of the bet."""
        return f"{self.bet_type.value} bet on {sorted(self.spaces)} for {self.amount}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the bet."""
        return f"Bet(type={self.bet_type.value}, spaces={sorted(self.spaces)}, amount={self.amount})"
