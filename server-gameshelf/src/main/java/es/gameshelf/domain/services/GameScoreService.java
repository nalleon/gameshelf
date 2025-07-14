package es.gameshelf.domain.services;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.GameScore;
import es.gameshelf.domain.Genre;
import es.gameshelf.domain.User;
import es.gameshelf.domain.interfaces.repository.IGameScoreRepository;
import es.gameshelf.domain.interfaces.service.IGameScoreService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service

public class GameScoreService implements IGameScoreService {
    /**
     * Properties
     */
    IGameScoreRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IGameScoreRepository repository) {
        this.repository = repository;
    }

    @Override
    public GameScore add(float score, User user, Game game) {
        GameScore item = new GameScore();
        item.setScore(score);
        item.setGame(game);
        item.setUser(user);

        return repository.save(item);
    }

    @Override
    public List<GameScore> findAll() {
        return repository.findAll();
    }

    @Override
    public GameScore findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public GameScore findByGame(Game game) {
        return repository.findByGame(game);
    }

    @Override
    public GameScore findByUser(User user) {
        return repository.findByUser(user);
    }

    @Override
    public float getAverageScorePerGame(Game game) {
        return repository.getAverageScorePerGame(game);
    }

    @Override
    public float getAverageScorePerUser(User user) {
        return repository.getAverageScorePerUser(user);
    }

    @Override
    public float getAverageScorePerGameGenre(Genre genre) {
        return repository.getAverageScorePerGameGenre(genre);
    }

    @Override
    public List<GameScore> findAllOrderedByHigherScore() {
        return repository.findAllOrderedByHigherScore();
    }

    @Override
    public List<GameScore> findAllOrderedByLowestScore() {
        return repository.findAllOrderedByLowestScore();
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public GameScore update(Integer id, float score, User user, Game game) {
        GameScore item = new GameScore(id);
        item.setScore(score);
        item.setGame(game);
        item.setUser(user);
        return repository.update(item);
    }
}
