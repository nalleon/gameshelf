package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.GameScore;
import es.gameshelf.domain.Genre;
import es.gameshelf.domain.User;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IGameScoreService {
    GameScore add(float score, User user, Game game);
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
    GameScore update(Integer id, float score, User user, Game game);
}
