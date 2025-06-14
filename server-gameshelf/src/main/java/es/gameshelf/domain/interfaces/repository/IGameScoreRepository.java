package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.GameScore;
import es.gameshelf.domain.Genre;
import es.gameshelf.domain.User;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IGameScoreRepository {
    GameScore save(GameScore gameScore);
    List<GameScore> findAll();
    GameScore findById(Integer id);
    GameScore findByGame(Game game);
    GameScore findByUser(User user);

    float getAverageScorePerGame(Game game);
    float getAverageScorePerUser(User user);

    float getAverageScorePerGameGenre(Genre genre);

    List<GameScore> findAllOrderedByHigherScore();
    List<GameScore> findAllOrderedByLowestScore();

    boolean delete(Integer id);
    GameScore update(GameScore gameScore);
}
