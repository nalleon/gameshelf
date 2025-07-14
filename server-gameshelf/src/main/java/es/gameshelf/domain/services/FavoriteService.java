package es.gameshelf.domain.services;

import es.gameshelf.domain.Favorite;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.User;
import es.gameshelf.domain.interfaces.repository.IFavoriteRepository;
import es.gameshelf.domain.interfaces.service.IFavoriteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class FavoriteService implements IFavoriteService {

    /**
     * Properties
     */
    IFavoriteRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IFavoriteRepository repository) {
        this.repository = repository;
    }

    @Override
    public Favorite add(User user, Game game) {
        Favorite item = new Favorite();
        item.setGame(game);
        item.setUser(user);
        return repository.save(item);
    }

    @Override
    public List<Favorite> findAll() {
        return repository.findAll();
    }

    @Override
    public List<Favorite> findAllByUser(User user) {
        return repository.findAllByUser(user);
    }

    @Override
    public List<Favorite> findAllByGame(Game game) {
        return repository.findAllByGame(game);
    }

    @Override
    public Favorite findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Game findMostFavoriteGame() {
        return repository.findMostFavoriteGame();
    }

    @Override
    public boolean checkIfIExists(User user, Game game) {
        return repository.checkIfIExists(user, game);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Favorite update(Integer id, User user, Game game) {
        Favorite item = new Favorite(id);
        item.setGame(game);
        item.setUser(user);
        return repository.update(item);
    }
}
