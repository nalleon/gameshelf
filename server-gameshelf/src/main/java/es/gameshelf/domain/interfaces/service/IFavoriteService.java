package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Favorite;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.User;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IFavoriteService {
    Favorite add(User user, Game game);
    List<Favorite> findAll();
    List<Favorite> findAllByUser(User user);
    List<Favorite> findAllByGame(Game game);
    Favorite findById(Integer id);
    Game findMostFavoriteGame();
    boolean checkIfIExists(User user, Game game);
    boolean delete(Integer id);
    Favorite update(Integer id, User user, Game game);
}
