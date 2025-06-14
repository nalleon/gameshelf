package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Favorite;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.User;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IFavoriteRepository {
    Favorite save(Favorite favorite);
    List<Favorite> findAll();
    Favorite findById(Integer id);
    Favorite checkIfIExists(User user, Game game);
    List<Favorite> findAllByUser(User user);
    List<Favorite> findAllByGame(Game game);
    boolean delete(Integer id);
    Favorite update(Favorite favorite);
}
