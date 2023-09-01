class HighScore:
    @classmethod
    def change_high_score(cls, player_score, high_score):
        if player_score > int(high_score):
            high_score_file = open("docs/high_score.txt", "w")
            high_score_file.write(str(player_score))
            high_score_file.close()
        
            return player_score
        
        return high_score