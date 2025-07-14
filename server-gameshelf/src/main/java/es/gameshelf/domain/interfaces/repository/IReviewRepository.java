package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Review;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.Status;
import es.gameshelf.domain.User;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IReviewRepository {
    Review save(Review review);
    List<Review> findAll();
    List<Review> findAllByUser(User user);
    List<Review> findAllByGame(Game game);
    List<Review> findAllByUserLatest(User user);
    List<Review> findAllByGameLatest(Game game);
    int countAllGroupedByGame(Game game);
    int countAllGroupedByUser(User user);

    Review findById(Integer id);
    boolean delete(Integer id);
    Review update(Review review);
}
